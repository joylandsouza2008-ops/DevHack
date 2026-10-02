"""
Rule-based risk classifier: turns one set of pond sensor readings into
Safe / Warning / Danger, and explains why in English and Kannada.

How it works:
  1. Load the threshold numbers from config/thresholds.toml.
  2. For each parameter, reject impossible readings as sensor faults.
  3. Convert units where needed (total ammonia -> toxic NH3, NO3 -> NO3-N).
  4. Grade each parameter: Safe if inside the safe range, Warning if inside
     the warning range, otherwise Danger.
  5. The pond's overall risk is the WORST grade among the parameters.

Example:
    from backend.risk_classifier import classify
    result = classify({"dissolved_oxygen": 2.5, "ph": 7.2, "temperature": 29})
    print(result.level)            # "danger"
    print(result.summary["en"])    # "Oxygen is very low (2.5 mg/L). ..."
    print(result.summary["kn"])    # same message in Kannada
"""

from __future__ import annotations

import math
import tomllib
from dataclasses import asdict, dataclass, field
from pathlib import Path

from backend import risk_messages as msg

# config/thresholds.toml, found relative to this file so it works from any folder
CONFIG_PATH = Path(__file__).resolve().parent.parent / "config" / "thresholds.toml"

# Higher number = worse. Used to find the worst parameter.
LEVEL_ORDER = {"safe": 0, "warning": 1, "danger": 2}


@dataclass
class ParameterResult:
    """The grade for one parameter, e.g. dissolved oxygen."""
    parameter: str          # key such as "dissolved_oxygen"
    name: dict              # display name {"en": ..., "kn": ...}
    reading: float          # value from the sensor, before any conversion
    value: float            # value compared with the thresholds (after conversion)
    unit: str               # unit of `value`
    level: str              # "safe", "warning", "danger", or "unknown" if it couldn't be checked
    direction: str | None   # "low" or "high" when outside the safe range, else None
    reason: dict            # {"en": ..., "kn": ...}; empty when safe


@dataclass
class RiskResult:
    """The overall result for one set of readings."""
    level: str                                         # worst level: "safe", "warning", "danger", or "unknown"
    level_name: dict                                   # {"en": "Danger", "kn": "ಅಪಾಯ"}
    causes: list = field(default_factory=list)         # parameters responsible for the overall level
    summary: dict = field(default_factory=dict)        # short explanation {"en": ..., "kn": ...}
    parameters: list = field(default_factory=list)     # one ParameterResult per graded parameter
    info: list = field(default_factory=list)           # shown to the farmer but not graded (turbidity)
    sensor_errors: list = field(default_factory=list)  # impossible readings that were ignored

    def to_dict(self) -> dict:
        """Plain dictionary, ready to send as JSON from the API."""
        return asdict(self)


def load_thresholds(path: Path = CONFIG_PATH) -> dict:
    """Read the threshold numbers from the TOML config file."""
    with open(path, "rb") as f:
        return tomllib.load(f)


def unionized_ammonia(total_ammonia: float, ph: float, temperature_c: float) -> float:
    """
    Return the toxic un-ionised ammonia (NH3) part of a total ammonia reading.

    Uses the standard equation from Emerson et al. (1975):
        pKa      = 0.09018 + 2729.92 / (temperature in kelvin)
        fraction = 1 / (10 ** (pKa - pH) + 1)
    Higher pH and warmer water mean a bigger toxic fraction.
    """
    pka = 0.09018 + 2729.92 / (temperature_c + 273.15)
    fraction = 1 / (10 ** (pka - ph) + 1)
    return total_ammonia * fraction


def in_range(value: float, rng: dict) -> bool:
    """True if `value` satisfies every limit (min / max / below) in `rng`."""
    if "min" in rng and value < rng["min"]:
        return False
    if "max" in rng and value > rng["max"]:
        return False
    if "below" in rng and value >= rng["below"]:
        return False
    return True


def _is_missing(value) -> bool:
    return value is None or (isinstance(value, float) and math.isnan(value))


def _fmt(value: float) -> str:
    """Short number for messages: 4.1, 34.0, 0.032."""
    return f"{value:.1f}" if abs(value) >= 1 else f"{value:.3f}"


def _grade(value: float, cfg: dict) -> tuple[str, str | None]:
    """Return (level, direction) for one value using its config section."""
    safe = cfg["safe"]
    if in_range(value, safe):
        return "safe", None
    direction = "low" if "min" in safe and value < safe["min"] else "high"
    level = "warning" if in_range(value, cfg["warning"]) else "danger"
    return level, direction


def _reason(parameter: str, direction: str, level: str, value: float, unit: str) -> dict:
    template = msg.REASONS.get((parameter, direction, level))
    if template is None:  # fallback so a new parameter never crashes the app
        name = msg.PARAMETER_NAMES.get(parameter, {"en": parameter, "kn": parameter})
        template = {lang: f"{name[lang]}: {{value}} {{unit}}" for lang in ("en", "kn")}
    return {lang: text.format(value=_fmt(value), unit=unit).strip() for lang, text in template.items()}


def classify(reading: dict, thresholds: dict | None = None) -> RiskResult:
    """
    Grade one set of readings.

    `reading` keys (any can be missing):
        dissolved_oxygen  mg/L
        ph
        temperature       °C
        ammonia           mg/L TOTAL ammonia (converted to NH3 here)
        nitrate           mg/L NO3 (converted to NO3-N here)
        turbidity         sensor units, information only
    """
    cfg = thresholds if thresholds is not None else load_thresholds()

    # Step 1: drop missing values and impossible readings (sensor faults).
    valid: dict[str, float] = {}
    sensor_errors = []
    for parameter, value in reading.items():
        if parameter not in cfg or _is_missing(value):
            continue
        value = float(value)
        if not in_range(value, cfg[parameter].get("plausible", {})):
            name = msg.PARAMETER_NAMES[parameter]
            sensor_errors.append({
                "parameter": parameter,
                "reading": value,
                "message": {lang: text.format(name=name[lang], value=_fmt(value))
                            for lang, text in msg.SENSOR_ERROR.items()},
            })
            continue
        valid[parameter] = value

    # Step 2: grade each valid parameter.
    graded: list[ParameterResult] = []
    info: list[ParameterResult] = []
    for parameter, reading_value in valid.items():
        p_cfg = cfg[parameter]
        name = msg.PARAMETER_NAMES[parameter]

        if not p_cfg.get("use_for_risk", True):
            info.append(ParameterResult(parameter, name, reading_value, reading_value,
                                        p_cfg["unit"], "unknown", None, {}))
            continue

        # Convert to the unit the thresholds are written in.
        value = reading_value
        if parameter == "ammonia":
            if "ph" not in valid or "temperature" not in valid:
                graded.append(ParameterResult(parameter, name, reading_value, reading_value,
                                              p_cfg["input_unit"], "unknown", None,
                                              dict(msg.AMMONIA_NEEDS_PH_AND_TEMPERATURE)))
                continue
            value = unionized_ammonia(reading_value, valid["ph"], valid["temperature"])
        elif parameter == "nitrate":
            value = reading_value * p_cfg["input_to_nitrogen_factor"]

        level, direction = _grade(value, p_cfg)
        reason = _reason(parameter, direction, level, value, p_cfg["unit"]) if direction else {}
        graded.append(ParameterResult(parameter, name, reading_value, value,
                                      p_cfg["unit"], level, direction, reason))

    # Step 3: overall level = worst graded parameter.
    checked = [p for p in graded if p.level in LEVEL_ORDER]
    if not checked:
        return RiskResult(level="unknown", level_name=msg.LEVEL_NAMES["unknown"],
                          summary=dict(msg.NO_VALID_READINGS), parameters=graded,
                          info=info, sensor_errors=sensor_errors)

    worst = max(checked, key=lambda p: LEVEL_ORDER[p.level]).level
    causes = [p for p in checked if p.level == worst] if worst != "safe" else []

    if causes:
        summary = {lang: " ".join(p.reason[lang] for p in causes) for lang in ("en", "kn")}
    else:
        summary = dict(msg.ALL_SAFE)

    return RiskResult(
        level=worst,
        level_name=msg.LEVEL_NAMES[worst],
        causes=[p.parameter for p in causes],
        summary=summary,
        parameters=graded,
        info=info,
        sensor_errors=sensor_errors,
    )
