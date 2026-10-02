"""
Experiment (not used by the app): forecast the AVERAGE dissolved oxygen over
the next 3 hours (and hours 3–6) instead of a single future reading, and
compare with the baselines. Results are written up in docs/do_forecast.md.

Run from the project folder:
    python -m ml.experiment_3h_average

Pass rule, fixed before running: the model must have >= 10% less error than
the BEST baseline. It did not (5.5%), so the app keeps the single-reading model.
"""

import pandas as pd

from backend.do_features import STEPS_PER_HOUR, build_features, to_regular_grid, FEATURES
from backend.risk_classifier import load_thresholds
from ml.train_do_forecast import (AVERAGE_WINDOWS, candidate_models, load_ponds, mae,
                                  reject_simulated, score, split_by_time)

WINDOW_STEPS = 3 * STEPS_PER_HOUR
REQUIRED_GAIN = 0.10   # model must beat the best baseline by at least 10%


def main() -> None:
    thresholds = load_thresholds()
    parts = []
    for station, readings in load_ponds(thresholds).items():
        reject_simulated(readings)
        grid = to_regular_grid(readings)
        feats = build_features(grid)
        do = grid["dissolved_oxygen"]
        # Average of the NEXT 3 hours (t+20 min ... t+3 h); needs at least 6 of the 9 readings.
        next_3h = do[::-1].rolling(WINDOW_STEPS, min_periods=6).mean()[::-1].shift(-1)
        for start in (0, 3):
            feats[f"target_{start}_{start + 3}h"] = next_3h.shift(-start * STEPS_PER_HOUR).reindex(feats.index)
        feats["station"] = station
        parts.append(feats)
    split = split_by_time(pd.concat(parts).rename_axis("ts").reset_index())

    for target in ("target_0_3h", "target_3_6h"):
        train, val, test = (split[p].dropna(subset=[target]) for p in ("train", "val", "test"))
        best_window = min(AVERAGE_WINDOWS, key=lambda c: mae(val[c], val[target]))
        val_mae = {}
        for name, model in candidate_models().items():
            model.fit(train[FEATURES], train[target])
            val_mae[name] = mae(model.predict(val[FEATURES]), val[target])
        chosen = min(val_mae, key=val_mae.get)
        model = candidate_models()[chosen]
        both = pd.concat([train, val])
        model.fit(both[FEATURES], both[target])

        results = {
            "DO stays the same": score(test["do_now"], test[target], thresholds),
            f"recent average ({best_window})": score(test[best_window], test[target], thresholds),
            f"model ({chosen})": score(model.predict(test[FEATURES]), test[target], thresholds),
        }
        print(f"\n{target}: {len(test)} test forecasts, {(test[target] < 5).mean() * 100:.1f}% truly below 5 mg/L")
        for name, s in results.items():
            print(f"  {name:32} off by {s['mae_mg_l']:.2f} mg/L on average")
        model_mae = list(results.values())[2]["mae_mg_l"]
        best_baseline = min(list(results.values())[:2], key=lambda s: s["mae_mg_l"])["mae_mg_l"]
        gain = 1 - model_mae / best_baseline
        verdict = "PASS" if gain >= REQUIRED_GAIN else "FAIL"
        print(f"  -> {gain * 100:.1f}% less error than the best baseline (needs {REQUIRED_GAIN * 100:.0f}%): {verdict}")


if __name__ == "__main__":
    main()
