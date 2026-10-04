"""
Demo data simulator. ONLY for driving the app demo — never for measuring
model accuracy (the training code refuses simulated data).

Why it exists: the real Pondsdata readings are dominated by sensor noise and
have no daily oxygen cycle, so they can't show how an early warning looks.
This simulator starts from the dataset's DAILY LEVELS (taken from
data/Ponds data.csv for the same calendar day and pond), keeps them inside
a healthy range so a normal day reads Safe, uses a typical coastal Karnataka
pond temperature, and adds the daily rhythm real ponds have:

  - Dissolved oxygen rises with sunlight (photosynthesis) from 06:00, peaks
    around 16:00, then falls slowly through the night to a dawn low.
  - Temperature peaks mid-afternoon; pH rises and falls with oxygen.
  - Scenario "oxygen_crash": on the first night, oxygen keeps sliding down to a
    dangerous level before dawn (the classic pond fish-kill pattern), then
    recovers in the morning. The Warning level is reached hours before Danger.

If data/Ponds data.csv is missing (e.g. a fresh clone or the online demo:
the dataset's licence is unknown, so it is not stored in git), fixed
FALLBACK_LEVELS are used instead, so the demo still runs.

Every reading is marked: column `source` = "simulated", and the DataFrame's
`attrs["source"]` = "simulated". The app must show SIMULATED_LABEL with it.

Example:
    from backend.simulator import simulate_readings
    df = simulate_readings("station1", start="2026-10-02 06:00", hours=48,
                           scenario="oxygen_crash")
"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

import numpy as np
import pandas as pd

from backend.do_features import STEP_MINUTES

DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "Ponds data.csv"

SIMULATED = "simulated"
SIMULATED_LABEL = {
    "en": "Simulated data",
    "kn": "ಅನುಕರಿಸಿದ (ಸಿಮ್ಯುಲೇಟೆಡ್) ಡೇಟಾ",
}
SCENARIOS = ("normal", "oxygen_crash")

# Daily-cycle settings (our judgement, typical of tropical fish ponds)
DO_AMPLITUDE_SHARE = 0.30          # day/night DO swing = ±30% of the daily level ...
DO_AMPLITUDE_RANGE = (1.0, 3.5)    # ... kept between ±1 and ±3.5 mg/L
POND_TEMPERATURE = 28.0            # °C daily average for a coastal Karnataka pond (judgement, not
                                   # from a source). Pondsdata comes from inland Andhra Pradesh, so
                                   # its temperatures are not used.
TEMP_AMPLITUDE = 1.5               # ±1.5 °C, warmest around 15:00 -> 26.5–29.5 °C

# Healthy range for the daily levels, so a normal day stays Safe once the daily
# cycle is added (Safe limits: config/thresholds.toml). Only the crash scenario
# should cause warnings.
HEALTHY_DAILY_RANGE = {
    "dissolved_oxygen": (8.6, None),  # dawn low = level - swing >= 6 mg/L (Safe >= 5)
    "ph": (7.0, 8.0),                 # ±0.3 daily swing (+ noise) stays inside 6.5–8.5
    "ammonia": (None, 0.10),          # total; toxic NH3 stays < 0.02 even at pH 8.3 and 29.5 °C
    "nitrate": (None, 40.0),          # NO3; = 9.0 mg/L NO3-N (Safe < 10)
}
# Used when data/Ponds data.csv is missing. Our own typical healthy values (judgement,
# not copied from the dataset), all inside HEALTHY_DAILY_RANGE. Same every day of the year.
FALLBACK_LEVELS = {
    "station1": {"dissolved_oxygen": 10.0, "temperature": POND_TEMPERATURE, "ph": 7.2,
                 "ammonia": 0.04, "nitrate": 20.0, "turbidity": 28.0},
    "station2": {"dissolved_oxygen": 10.5, "temperature": POND_TEMPERATURE, "ph": 7.3,
                 "ammonia": 0.05, "nitrate": 22.0, "turbidity": 28.0},
    "station3": {"dissolved_oxygen": 11.0, "temperature": POND_TEMPERATURE, "ph": 7.0,
                 "ammonia": 0.08, "nitrate": 35.0, "turbidity": 38.0},
}
PH_AMPLITUDE = 0.3                 # ±0.3, follows oxygen
CRASH_LOWEST_DO = 1.8              # mg/L reached at ~04:30 in the crash scenario

# Small sensor noise (standard deviation)
NOISE = {"dissolved_oxygen": 0.15, "temperature": 0.05, "ph": 0.02,
         "ammonia": 0.005, "nitrate": 0.5, "turbidity": 0.5}

COLUMNS = {"DO": "dissolved_oxygen", "TEMP": "temperature", "PH": "ph",
           "AMMONIA(mg/l)": "ammonia", "NITRATE(PPM)": "nitrate", "TURBIDITY": "turbidity"}


def is_simulated(df: pd.DataFrame) -> bool:
    """True if a DataFrame (or any row in it) came from this simulator."""
    if df.attrs.get("source") == SIMULATED:
        return True
    return "source" in df.columns and (df["source"] == SIMULATED).any()


def reject_simulated(df: pd.DataFrame) -> None:
    """Stop with an error if simulated data reaches model training or evaluation."""
    if is_simulated(df):
        raise ValueError("Simulated data must never be used to train or measure the model.")


@lru_cache(maxsize=1)
def daily_levels(path: Path = DATA_FILE) -> pd.DataFrame:
    """
    Median reading per pond per calendar day from Pondsdata, smoothed over 3 days.
    Index: (station, "MM-DD"); columns: dissolved_oxygen, temperature, ph,
    ammonia, nitrate, turbidity.
    """
    if not path.exists():
        raise FileNotFoundError(f"{path} not found. See README.md for dataset download steps.")
    raw = pd.read_csv(path, low_memory=False).dropna(subset=["station", "Date"])
    raw["station"] = raw["station"].str.lower()
    raw["day"] = pd.to_datetime(raw["Date"], format="%d-%m-%Y")
    for col in COLUMNS:
        raw[col] = pd.to_numeric(raw[col], errors="coerce")
    # Ignore impossible zero readings when computing typical levels.
    raw.loc[raw["DO"] <= 0, "DO"] = np.nan
    raw.loc[raw["TEMP"] <= 0, "TEMP"] = np.nan

    levels = []
    for station, g in raw.groupby("station"):
        daily = g.groupby("day")[list(COLUMNS)].median().rename(columns=COLUMNS)
        daily = daily.rolling(3, min_periods=1, center=True).median()
        daily.index = daily.index.strftime("%m-%d")
        daily = daily.groupby(level=0).mean()          # one row per calendar day
        daily["station"] = station
        levels.append(daily)
    return pd.concat(levels).reset_index(names="month_day").set_index(["station", "month_day"])


def fallback_levels() -> pd.DataFrame:
    """FALLBACK_LEVELS as a daily-level table (one "01-01" row per pond, used for every day)."""
    return (pd.DataFrame.from_dict(FALLBACK_LEVELS, orient="index")
            .rename_axis("station").assign(month_day="01-01")
            .set_index("month_day", append=True))


def _level_for(levels: pd.DataFrame, station: str, day: pd.Timestamp) -> pd.Series:
    """Daily level for a pond on the same calendar day (any year)."""
    table = levels.loc[station]
    key = day.strftime("%m-%d")
    if key not in table.index:   # e.g. 29 Feb or a day the pond has no data: use the nearest day
        doy = day.dayofyear
        days = pd.to_datetime("2001-" + table.index, format="%Y-%m-%d").dayofyear
        key = table.index[np.argmin(np.minimum(abs(days - doy), 365 - abs(days - doy)))]
    return table.loc[key]


def _oxygen_shape(hour: np.ndarray) -> np.ndarray:
    """-1 at 06:00 (dawn low) ... +1 at 16:00 (afternoon high); slow fall overnight."""
    rising = (hour >= 6) & (hour < 16)
    since_peak = (hour - 16) % 24                       # 0 at 16:00 ... 14 at 06:00
    return np.where(rising, -np.cos(np.pi * (hour - 6) / 10), np.cos(np.pi * since_peak / 14))


def _crash_weight(times: pd.DatetimeIndex, start: pd.Timestamp) -> np.ndarray:
    """0..1 weight of the night oxygen crash on the first night after `start`."""
    night = start.normalize() + pd.Timedelta(hours=20)
    if start >= night:
        night += pd.Timedelta(days=1)
    hours = (times - night) / pd.Timedelta(hours=1)     # 0 at 20:00
    w = np.interp(hours, [0, 8.5, 9.5, 12], [0, 1, 1, 0], left=0, right=0)  # worst 04:30–05:30, gone by 08:00
    return w


def simulate_readings(station: str = "station1", start="2026-10-02 06:00", hours: int = 48,
                      scenario: str = "normal", seed: int = 0,
                      levels: pd.DataFrame | None = None) -> pd.DataFrame:
    """
    Simulated readings every 20 minutes for one pond.

    station:  "station1", "station2" or "station3" (whose daily levels to use)
    start:    first reading time; daily levels come from the same calendar day
    hours:    how many hours to generate
    scenario: "normal" or "oxygen_crash"
    seed:     same seed -> same numbers, so the demo is repeatable
    levels:   optional daily-level table (for tests); default reads Pondsdata,
              or FALLBACK_LEVELS if it isn't downloaded
    """
    if scenario not in SCENARIOS:
        raise ValueError(f"scenario must be one of {SCENARIOS}")
    if levels is None:
        levels = daily_levels() if DATA_FILE.exists() else fallback_levels()
    start = pd.Timestamp(start).floor(f"{STEP_MINUTES}min")
    times = pd.date_range(start, periods=hours * 60 // STEP_MINUTES, freq=f"{STEP_MINUTES}min")
    rng = np.random.default_rng(seed)

    base = pd.DataFrame([_level_for(levels, station, t.normalize()) for t in times], index=times)
    for col, (low, high) in HEALTHY_DAILY_RANGE.items():
        base[col] = base[col].clip(lower=low, upper=high)
    base["temperature"] = POND_TEMPERATURE
    hour = (times.hour + times.minute / 60).to_numpy()
    shape = _oxygen_shape(hour)

    amp = np.clip(base["dissolved_oxygen"] * DO_AMPLITUDE_SHARE, *DO_AMPLITUDE_RANGE)
    do = base["dissolved_oxygen"] + amp * shape
    if scenario == "oxygen_crash":
        w = _crash_weight(times, start)
        do = do * (1 - w) + CRASH_LOWEST_DO * w

    out = pd.DataFrame({
        "dissolved_oxygen": do,
        "temperature": base["temperature"] + TEMP_AMPLITUDE * np.cos(2 * np.pi * (hour - 15) / 24),
        "ph": base["ph"] + PH_AMPLITUDE * shape,
        "ammonia": base["ammonia"],
        "nitrate": base["nitrate"],
        "turbidity": base["turbidity"],
    }, index=times)
    for col, sd in NOISE.items():
        out[col] = out[col] + rng.normal(0, sd, len(out))
    out = out.clip(lower=0).round({"dissolved_oxygen": 2, "temperature": 2, "ph": 2,
                                   "ammonia": 3, "nitrate": 1, "turbidity": 1})
    out["source"] = SIMULATED
    out.attrs["source"] = SIMULATED
    out.attrs["label"] = SIMULATED_LABEL
    out.attrs["scenario"] = scenario
    return out
