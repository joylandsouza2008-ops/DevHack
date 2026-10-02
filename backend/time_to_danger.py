"""
"Time until danger": if dissolved oxygen (DO) has been falling over the last
1–2 hours, estimate when it will reach the Danger level (3 mg/L) and say so
in plain words, in English and Kannada.

How it works:
  1. Take the DO readings from the last `window_hours` (config/thresholds.toml).
  2. Fit a straight line through them (least squares). Its slope is how fast
     DO is changing, in mg/L per hour.
  3. Check the readings really follow that line (R², "how straight": 1 = all
     on the line, 0 = no pattern). Below `min_r_squared` the readings are
     just jumping around, so we don't call it a fall.
  4. If DO is falling faster than `min_fall_per_hour`, extend the line to see
     when it reaches the Danger level. Only report it if that is within
     `max_hours_ahead`.

This is a simple trend, not a forecast model: it assumes the recent fall
continues, which is how night-time oxygen crashes usually develop.

Example:
    from backend.time_to_danger import estimate_time_to_danger
    est = estimate_time_to_danger(do_series)    # pandas Series of DO, indexed by time
    est["status"]          # e.g. "danger_expected"
    est["message"]["en"]   # "Oxygen is falling (about 1.2 mg/L per hour). ..."
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from backend import risk_messages as msg
from backend.risk_classifier import load_thresholds

STATUSES = ("danger_expected", "already_danger", "falling_slowly", "not_falling", "not_enough_data")


def _duration(hours: float) -> tuple[str, str]:
    """Plain-words duration: 'about 40 minutes' / 'about 2.5 hours', in English and Kannada."""
    if hours < 1:
        minutes = max(10, int(round(hours * 60 / 10)) * 10)
        return f"about {minutes} minutes", f"ಸುಮಾರು {minutes} ನಿಮಿಷಗಳಲ್ಲಿ"
    rounded = round(hours * 2) / 2                     # nearest half hour
    text = f"{rounded:g}"
    unit = "hour" if rounded == 1 else "hours"
    return f"about {text} {unit}", f"ಸುಮಾರು {text} ಗಂಟೆಗಳಲ್ಲಿ"


def _message(status: str, **values) -> dict:
    return {lang: text.format(**values) for lang, text in msg.TIME_TO_DANGER[status].items()}


def estimate_time_to_danger(dissolved_oxygen: pd.Series, thresholds: dict | None = None) -> dict:
    """
    `dissolved_oxygen`: DO readings (mg/L) indexed by timestamp, oldest first.
    Missing readings (NaN) are ignored.

    Returns a dict:
        status            one of STATUSES
        hours_to_danger   e.g. 2.3 (only when status == "danger_expected")
        danger_at         ISO time of the estimated crossing (same condition)
        rate_mg_l_per_hour  slope of the trend (negative = falling)
        message           {"en": ..., "kn": ...}
    """
    cfg = thresholds if thresholds is not None else load_thresholds()
    ttd = cfg["time_to_danger"]
    danger = cfg["dissolved_oxygen"]["warning"]["min"]       # below this = Danger (3 mg/L)

    result = {"status": "not_enough_data", "hours_to_danger": None, "danger_at": None,
              "rate_mg_l_per_hour": None, "trend_r_squared": None, "danger_level_mg_l": danger}

    do = dissolved_oxygen.dropna().sort_index()
    if do.empty:
        return {**result, "message": _message("not_enough_data")}
    now = do.index[-1]
    recent = do[do.index > now - pd.Timedelta(hours=ttd["window_hours"])]
    span = (recent.index[-1] - recent.index[0]) / pd.Timedelta(hours=1)
    if len(recent) < ttd["min_readings"] or span < ttd["min_span_hours"]:
        return {**result, "message": _message("not_enough_data")}

    # Straight-line fit: DO = slope * hours + intercept, with hours counted back from now (now = 0).
    hours = ((recent.index - now) / pd.Timedelta(hours=1)).to_numpy()
    values = recent.to_numpy()
    slope, level_now = np.polyfit(hours, values, 1)
    fitted = slope * hours + level_now
    total = np.sum((values - values.mean()) ** 2)
    r_squared = 1 - np.sum((values - fitted) ** 2) / total if total > 0 else 0.0
    result["rate_mg_l_per_hour"] = round(float(slope), 2)
    result["trend_r_squared"] = round(float(r_squared), 2)

    if recent.iloc[-1] < danger or level_now < danger:
        return {**result, "status": "already_danger", "message": _message("already_danger")}
    if slope > -ttd["min_fall_per_hour"] or r_squared < ttd["min_r_squared"]:
        return {**result, "status": "not_falling", "message": _message("not_falling")}

    hours_left = (level_now - danger) / -slope
    if hours_left > ttd["max_hours_ahead"]:
        return {**result, "status": "falling_slowly",
                "message": _message("falling_slowly", hours=f"{ttd['max_hours_ahead']:g}")}

    danger_at = now + pd.Timedelta(hours=hours_left)
    duration_en, duration_kn = _duration(hours_left)
    return {
        **result,
        "status": "danger_expected",
        "hours_to_danger": round(float(hours_left), 2),
        "danger_at": danger_at.isoformat(),
        "message": _message("danger_expected", rate=f"{-slope:.1f}", danger=f"{danger:g}",
                            duration=duration_en, duration_kn=duration_kn,
                            # A rough estimate: say "around 02:00", not "around 01:59".
                            clock=danger_at.round("10min").strftime("%H:%M")),
    }
