"""
Dissolved-oxygen forecast for the app.

Loads the model trained by ml/train_do_forecast.py, predicts DO 1, 3 and
6 hours ahead from a pond's last 24 hours of readings, and turns each
prediction into a future risk level with the rule-based classifier.

Example:
    from backend.do_forecast import forecast_do
    forecasts = forecast_do(readings)   # readings: DataFrame, see below
    forecasts[1]["predicted_do"]        # e.g. 12.4 (3 h ahead)
    forecasts[1]["risk"]["level"]       # e.g. "safe"
"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

import joblib
import pandas as pd

from backend.do_features import build_features, to_regular_grid
from backend.risk_classifier import classify

MODEL_FILE = Path(__file__).resolve().parent.parent / "models" / "do_forecast.joblib"


@lru_cache(maxsize=1)
def load_model(path: Path = MODEL_FILE) -> dict:
    """Load the saved model bundle once and keep it in memory."""
    if not path.exists():
        raise FileNotFoundError(f"{path} not found. Train it with: python -m ml.train_do_forecast")
    return joblib.load(path)


def forecast_do(readings: pd.DataFrame, bundle: dict | None = None) -> list[dict]:
    """
    Forecast DO for each horizon in the model (1, 3 and 6 hours).

    `readings`: one pond's recent sensor readings, indexed by timestamp
    (ideally the last 24 hours), with columns
        dissolved_oxygen (mg/L), temperature (°C), ph

    Returns one dict per horizon:
        hours_ahead, for_time, predicted_do, expected_error_mg_l, risk
    where `risk` is the rule-based classifier's result for the predicted DO.
    """
    bundle = bundle if bundle is not None else load_model()

    grid = to_regular_grid(readings)
    features = build_features(grid)
    if features.empty or features.index[-1] != grid.index[-1]:
        raise ValueError("Not enough recent DO readings (need at least half of the last 3 hours).")

    latest = features.iloc[[-1]][bundle["features"]]   # double brackets keep it a 1-row table
    now = features.index[-1]

    results = []
    for hours in bundle["horizons_hours"]:
        predicted = float(bundle["models"][hours].predict(latest)[0])
        results.append({
            "hours_ahead": hours,
            "for_time": (now + pd.Timedelta(hours=hours)).isoformat(),
            "predicted_do": round(predicted, 2),
            # Average test-period error: show it so farmers know how sure we are.
            "expected_error_mg_l": bundle["test_mae_mg_l"][hours],
            "risk": classify({"dissolved_oxygen": predicted}).to_dict(),
        })
    return results
