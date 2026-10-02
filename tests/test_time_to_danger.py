"""
Tests for the "time until danger" estimate.

Run from the project folder with:   python -m pytest
"""

import numpy as np
import pandas as pd

from backend.simulator import simulate_readings
from backend.time_to_danger import estimate_time_to_danger
from tests.test_simulator import LEVELS


def do_series(values, end="2026-10-03 01:00"):
    """DO readings every 20 minutes ending at `end`."""
    times = pd.date_range(end=end, periods=len(values), freq="20min")
    return pd.Series(values, index=times, dtype="float64")


def test_steady_fall_gives_time_and_clock():
    # Falls 1.2 mg/L per hour (0.4 per 20 min), now at 5.4 -> reaches 3 in 2 hours, at 03:00.
    est = estimate_time_to_danger(do_series([7.4, 7.0, 6.6, 6.2, 5.8, 5.4]))
    assert est["status"] == "danger_expected"
    assert abs(est["hours_to_danger"] - 2.0) < 0.05
    assert est["danger_at"].startswith("2026-10-03T03:00")
    assert "about 2 hours, around 03:00" in est["message"]["en"]
    assert "ಸುಮಾರು 2 ಗಂಟೆಗಳಲ್ಲಿ (03:00 ಹೊತ್ತಿಗೆ)" in est["message"]["kn"]


def test_clock_time_is_rounded_to_10_minutes():
    # Now 01:00 at 5.5, falling 1.2 mg/L per hour -> 3 mg/L at about 03:05 -> "around 03:10".
    est = estimate_time_to_danger(do_series([7.5, 7.1, 6.7, 6.3, 5.9, 5.5]))
    assert "around 03:10" in est["message"]["en"] or "around 03:00" in est["message"]["en"]
    assert est["message"]["en"].split("around ")[1][3:5] in {"00", "10", "20", "30", "40", "50"}


def test_short_time_is_said_in_minutes():
    est = estimate_time_to_danger(do_series([5.6, 5.2, 4.8, 4.4, 4.0, 3.6]))
    assert est["status"] == "danger_expected"
    assert "about 30 minutes" in est["message"]["en"]
    assert "ನಿಮಿಷಗಳಲ್ಲಿ" in est["message"]["kn"]


def test_steady_or_rising_oxygen_is_not_falling():
    assert estimate_time_to_danger(do_series([8.0] * 6))["status"] == "not_falling"
    assert estimate_time_to_danger(do_series([6, 6.5, 7, 7.5, 8, 8.5]))["status"] == "not_falling"


def test_slow_fall_far_from_danger():
    # Falling 0.6 mg/L per hour from 12 mg/L: 15 hours away -> beyond the 6 h limit.
    est = estimate_time_to_danger(do_series([13.0, 12.8, 12.6, 12.4, 12.2, 12.0]))
    assert est["status"] == "falling_slowly"
    assert "next 6 hours" in est["message"]["en"]


def test_noisy_jumps_are_not_called_a_fall():
    # Like real Pondsdata: big random jumps, no steady trend.
    est = estimate_time_to_danger(do_series([10.4, 8.3, 6.3, 6.4, 10.1, 6.1]))
    assert est["status"] == "not_falling"
    assert est["trend_r_squared"] < 0.6


def test_already_below_danger():
    est = estimate_time_to_danger(do_series([4.0, 3.6, 3.3, 3.1, 2.9, 2.7]))
    assert est["status"] == "already_danger"


def test_too_few_readings():
    assert estimate_time_to_danger(do_series([7.0, 6.0]))["status"] == "not_enough_data"
    gappy = do_series([7.4, np.nan, np.nan, np.nan, np.nan, 5.4])
    assert estimate_time_to_danger(gappy)["status"] == "not_enough_data"


def test_crash_scenario_warns_hours_ahead_and_converges():
    do = simulate_readings(start="2026-10-02 06:00", hours=30, scenario="oxygen_crash",
                           levels=LEVELS)["dissolved_oxygen"]
    real_crossing = do[do < 3].index.min()
    alerts = [t for t in do.index[do.index < real_crossing]
              if estimate_time_to_danger(do[:t])["status"] == "danger_expected"]
    assert real_crossing - alerts[0] >= pd.Timedelta(hours=3), "first alert at least 3 h ahead"
    # One hour before the real crossing, the estimate is within 30 minutes of it.
    est = estimate_time_to_danger(do[: real_crossing - pd.Timedelta(hours=1)])
    assert abs(pd.Timestamp(est["danger_at"]) - real_crossing) <= pd.Timedelta(minutes=30)


def test_normal_scenario_never_predicts_danger():
    do = simulate_readings(start="2026-10-02 00:00", hours=48, levels=LEVELS)["dissolved_oxygen"]
    statuses = {estimate_time_to_danger(do[:t])["status"] for t in do.index[6:]}
    assert "danger_expected" not in statuses
