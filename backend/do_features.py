"""
Feature building for the dissolved-oxygen (DO) forecast.

A "feature" is one number the model looks at to make a prediction, e.g.
"average DO over the last 3 hours". This file is shared by training
(ml/train_do_forecast.py) and the app (backend/do_forecast.py) so both
compute features in exactly the same way.

Input: one pond's readings on a regular 20-minute grid, oldest first,
as a pandas DataFrame indexed by timestamp with columns:
    dissolved_oxygen, temperature, ph     (missing readings = NaN)
"""

from __future__ import annotations

import numpy as np
import pandas as pd

STEP_MINUTES = 20            # sensor reading interval in Pondsdata
STEPS_PER_HOUR = 60 // STEP_MINUTES
HISTORY_STEPS = 24 * STEPS_PER_HOUR   # the model needs the last 24 hours

# How far ahead we forecast, in hours.
HORIZONS_HOURS = [1, 3, 6]

FEATURES = [
    "do_now",          # latest DO reading
    "do_mean_1h",      # average DO, last 1 hour
    "do_mean_3h",      # average DO, last 3 hours
    "do_mean_6h",      # average DO, last 6 hours
    "do_mean_24h",     # average DO, last 24 hours (the pond's current "level")
    "do_std_3h",       # how much DO jumped around in the last 3 hours
    "temp_mean_3h",    # average water temperature, last 3 hours
    "ph_mean_3h",      # average pH, last 3 hours
    "hour_sin",        # time of day, encoded so 23:40 and 00:00 are close
    "hour_cos",
]

# A feature row is only built if at least this share of the last 3 hours of DO
# readings exist; otherwise the forecast would be guesswork.
MIN_RECENT_COVERAGE = 0.5


def to_regular_grid(df: pd.DataFrame) -> pd.DataFrame:
    """Put readings on an exact 20-minute grid; gaps become NaN rows."""
    df = df.sort_index()
    df = df[~df.index.duplicated(keep="last")]
    grid = pd.date_range(df.index.min().floor(f"{STEP_MINUTES}min"),
                         df.index.max().floor(f"{STEP_MINUTES}min"),
                         freq=f"{STEP_MINUTES}min")
    return df.reindex(grid)


def build_features(grid: pd.DataFrame) -> pd.DataFrame:
    """
    One feature row per timestamp, using only readings at or before it
    (never the future). Rows without enough recent data are dropped.
    """
    do = grid["dissolved_oxygen"]
    h = STEPS_PER_HOUR

    def mean(series, steps):
        return series.rolling(steps, min_periods=1).mean()

    hour = grid.index.hour + grid.index.minute / 60
    feats = pd.DataFrame({
        "do_now": do.ffill(limit=h),          # carry the last reading forward for up to 1 h
        "do_mean_1h": mean(do, 1 * h),
        "do_mean_3h": mean(do, 3 * h),
        "do_mean_6h": mean(do, 6 * h),
        "do_mean_24h": mean(do, 24 * h),
        "do_std_3h": do.rolling(3 * h, min_periods=2).std(),
        "temp_mean_3h": mean(grid["temperature"], 3 * h),
        "ph_mean_3h": mean(grid["ph"], 3 * h),
        "hour_sin": np.sin(2 * np.pi * hour / 24),
        "hour_cos": np.cos(2 * np.pi * hour / 24),
    }, index=grid.index)

    coverage = do.notna().rolling(3 * h, min_periods=1).mean()
    feats = feats[coverage >= MIN_RECENT_COVERAGE]
    # Temperature / pH may be missing; fall back to typical values rather than
    # dropping the row (they matter far less than DO itself).
    feats["temp_mean_3h"] = feats["temp_mean_3h"].fillna(27.0)
    feats["ph_mean_3h"] = feats["ph_mean_3h"].fillna(7.0)
    return feats.dropna()[FEATURES]
