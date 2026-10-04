"""
Tests for the demo data simulator.

Run from the project folder with:   python -m pytest
Most tests use a small made-up table of daily levels, so they run even
without the datasets. The last test uses the real Pondsdata if present.
"""

import pandas as pd
import pytest

from backend.risk_classifier import classify
from backend.simulator import (DATA_FILE, SIMULATED_LABEL, fallback_levels, is_simulated,
                               reject_simulated, simulate_readings)


def make_levels(do=12.5, ph=6.8, ammonia=0.04, nitrate=28.0, temperature=25.5, turbidity=30.0):
    """Daily-level table in the simulator's format: same values for every day of the year."""
    days = pd.date_range("2001-01-01", "2001-12-31").strftime("%m-%d")
    rows = [{"station": "station1", "month_day": d, "dissolved_oxygen": do, "temperature": temperature,
             "ph": ph, "ammonia": ammonia, "nitrate": nitrate, "turbidity": turbidity} for d in days]
    return pd.DataFrame(rows).set_index(["station", "month_day"])


LEVELS = make_levels()


def risk_levels(df):
    """Rule-based risk level for every simulated reading."""
    return df.apply(lambda row: classify(row.drop("source").to_dict()).level, axis=1)


# --- Labelling: simulated data must always say so -----------------------

def test_every_reading_is_labelled_simulated():
    df = simulate_readings(start="2026-10-02 06:00", hours=24, levels=LEVELS)
    assert (df["source"] == "simulated").all()
    assert df.attrs["source"] == "simulated"
    assert df.attrs["label"] == SIMULATED_LABEL
    assert SIMULATED_LABEL["en"] == "Simulated data"
    assert is_simulated(df)


def test_simulated_data_is_refused_for_training():
    with pytest.raises(ValueError, match="never be used"):
        reject_simulated(simulate_readings(hours=6, levels=LEVELS))


def test_training_pipeline_refuses_simulated_ponds():
    from ml.train_do_forecast import make_table
    df = simulate_readings(hours=24, levels=LEVELS)
    with pytest.raises(ValueError, match="never be used"):
        make_table({"station1": df})


def test_real_style_data_is_not_flagged():
    real = pd.DataFrame({"dissolved_oxygen": [8.0]}, index=[pd.Timestamp("2022-02-01")])
    assert not is_simulated(real)
    reject_simulated(real)   # no error


# --- Behaviour ----------------------------------------------------------

def test_same_seed_gives_same_demo():
    a = simulate_readings(hours=12, seed=7, levels=LEVELS)
    b = simulate_readings(hours=12, seed=7, levels=LEVELS)
    c = simulate_readings(hours=12, seed=8, levels=LEVELS)
    pd.testing.assert_frame_equal(a, b)
    assert not a["dissolved_oxygen"].equals(c["dissolved_oxygen"])


def test_oxygen_lowest_at_dawn_highest_in_afternoon():
    df = simulate_readings(start="2026-10-02 00:00", hours=24, levels=LEVELS)
    do = df["dissolved_oxygen"]
    assert 4 <= do.idxmin().hour <= 7
    assert 14 <= do.idxmax().hour <= 18


def test_temperature_is_coastal_karnataka_range():
    temp = simulate_readings(start="2026-10-02 00:00", hours=48, levels=LEVELS)["temperature"]
    assert 26.0 <= temp.min() and temp.max() <= 30.0


def test_normal_scenario_is_safe_even_with_poor_dataset_levels():
    # Levels like Pondsdata in Feb–Apr (low oxygen, acidic, cool, high nitrate) are
    # nudged into the healthy range, so a normal day never triggers a warning.
    poor = make_levels(do=4.6, ph=5.6, ammonia=0.34, nitrate=54.0, temperature=24.0)
    df = simulate_readings(start="2026-03-15 00:00", hours=72, levels=poor)
    assert set(risk_levels(df)) == {"safe"}


def test_crash_scenario_warns_hours_before_danger_then_recovers():
    df = simulate_readings(start="2026-10-02 06:00", hours=36, scenario="oxygen_crash", levels=LEVELS)
    levels = risk_levels(df)
    first_warning = levels[levels == "warning"].index.min()
    first_danger = levels[levels == "danger"].index.min()
    assert pd.notna(first_danger), "crash must reach Danger"
    assert first_danger - first_warning >= pd.Timedelta(hours=1), "Warning must come well before Danger"
    assert levels[: first_warning].iloc[:-1].eq("safe").all(), "Safe until the crash starts"
    assert levels["2026-10-03 12:00":].eq("safe").all(), "pond recovers by the next afternoon"
    # The alert names oxygen as the cause.
    danger_row = df.loc[first_danger].drop("source").to_dict()
    assert classify(danger_row).causes == ["dissolved_oxygen"]


def test_unknown_scenario_is_an_error():
    with pytest.raises(ValueError):
        simulate_readings(scenario="tsunami", levels=LEVELS)


# --- Without the dataset (fresh clone / online demo) ---------------------

@pytest.mark.parametrize("station", ["station1", "station2", "station3"])
def test_fallback_levels_normal_is_safe_and_crash_reaches_danger(station):
    normal = simulate_readings(station, start="2026-10-02 06:00", hours=48, levels=fallback_levels())
    crash = simulate_readings(station, start="2026-10-02 06:00", hours=48, scenario="oxygen_crash",
                              levels=fallback_levels())
    assert set(risk_levels(normal)) == {"safe"}
    assert "danger" in set(risk_levels(crash))
    assert is_simulated(normal) and is_simulated(crash)


# --- With the real dataset ----------------------------------------------

@pytest.mark.skipif(not DATA_FILE.exists(), reason="Pondsdata not downloaded (see README)")
@pytest.mark.parametrize("station", ["station1", "station2", "station3"])
def test_normal_scenario_is_safe_all_year_with_real_levels(station):
    for start in ["2026-02-10", "2026-04-15", "2026-05-20", "2026-08-01", "2026-10-02", "2026-12-25"]:
        df = simulate_readings(station, start=start, hours=48)
        assert set(risk_levels(df)) == {"safe"}, f"{station} {start}"
