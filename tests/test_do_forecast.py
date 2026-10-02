"""
Tests for the DO forecast: feature building, the saved model, and the
link to the rule-based classifier.

Run from the project folder with:   python -m pytest
"""

import numpy as np
import pandas as pd
import pytest

from backend.do_features import FEATURES, HISTORY_STEPS, build_features, to_regular_grid
from backend.do_forecast import MODEL_FILE, forecast_do, load_model


def pond_readings(do_level=8.0, hours=24, end="2022-12-10 12:00"):
    """A pond's last `hours` of readings every 20 minutes, with a little noise."""
    times = pd.date_range(end=end, periods=hours * 3, freq="20min")
    rng = np.random.default_rng(0)
    return pd.DataFrame({
        "dissolved_oxygen": do_level + rng.normal(0, 0.3, len(times)),
        "temperature": 28.0,
        "ph": 7.2,
    }, index=times)


class FixedModel:
    """Stand-in model that always predicts the same DO, so tests control the outcome."""
    def __init__(self, value):
        self.value = value

    def predict(self, X):
        return np.full(len(X), self.value)


def fake_bundle(value):
    return {"models": {1: FixedModel(value), 3: FixedModel(value), 6: FixedModel(value)},
            "features": FEATURES, "horizons_hours": [1, 3, 6],
            "test_mae_mg_l": {1: 4.5, 3: 4.5, 6: 4.5}}


# --- Features -----------------------------------------------------------

def test_history_is_24_hours():
    assert HISTORY_STEPS == 72


def test_features_never_use_future_readings():
    # Adding later readings must not change the features for an earlier time.
    full = pond_readings(hours=24)
    early = full.iloc[:-9]                       # same data minus the last 3 hours
    f_full = build_features(to_regular_grid(full))
    f_early = build_features(to_regular_grid(early))
    t = f_early.index[-1]
    pd.testing.assert_series_equal(f_full.loc[t], f_early.loc[t])


def test_gaps_become_missing_rows_not_shifted_data():
    readings = pond_readings(hours=6).drop(pond_readings(hours=6).index[5:8])
    grid = to_regular_grid(readings)
    assert len(grid) == 18                       # 6 hours x 3 readings, gap filled with NaN rows
    assert grid["dissolved_oxygen"].isna().sum() == 3


# --- Forecast + classifier ----------------------------------------------

def test_predicted_low_do_becomes_danger():
    out = forecast_do(pond_readings(), bundle=fake_bundle(2.0))
    assert [f["hours_ahead"] for f in out] == [1, 3, 6]
    assert all(f["risk"]["level"] == "danger" for f in out)
    assert "Oxygen is very low" in out[0]["risk"]["summary"]["en"]


def test_predicted_ok_do_is_safe():
    out = forecast_do(pond_readings(), bundle=fake_bundle(7.5))
    assert {f["risk"]["level"] for f in out} == {"safe"}
    assert out[1]["for_time"] == "2022-12-10T15:00:00"   # 3 h after the last reading


def test_too_few_recent_readings_is_an_error():
    readings = pond_readings()
    readings.iloc[-9:, readings.columns.get_loc("dissolved_oxygen")] = np.nan  # last 3 h of DO missing
    with pytest.raises(ValueError):
        forecast_do(readings, bundle=fake_bundle(7.5))


# --- The real saved model -------------------------------------------------

needs_model = pytest.mark.skipif(not MODEL_FILE.exists(), reason="run python -m ml.train_do_forecast first")


@needs_model
def test_saved_model_loads_and_predicts_plausible_do():
    bundle = load_model()
    assert bundle["horizons_hours"] == [1, 3, 6]
    assert bundle["features"] == FEATURES
    out = forecast_do(pond_readings(do_level=10.0))
    for f in out:
        assert 0 < f["predicted_do"] < 30
        assert f["risk"]["level"] in {"safe", "warning", "danger"}
