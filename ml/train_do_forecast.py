"""
Train the dissolved-oxygen (DO) forecast model on Pondsdata.

Run from the project folder:
    python -m ml.train_do_forecast

What it does, step by step:
  1. Load data/Ponds data.csv and clean it (fix text values, drop sensor faults).
  2. Put each pond's readings on a regular 20-minute timeline.
  3. Build features from the past (backend/do_features.py) and targets:
     the actual DO 1, 3 and 6 hours later.
  4. Split by time: first 70% = train, next 15% = validation, last 15% = test.
     The model never sees the test period while training.
  5. Compare four ways of forecasting on the validation period:
       - "DO stays the same"   (persistence baseline)
       - "recent average"      (average of the last few hours, best window)
       - linear model          (Ridge regression: explainable weights)
       - gradient boosting     (decision trees: can learn non-linear patterns)
     Keep whichever model is more accurate; retrain it on train + validation.
  6. Score everything on the test period, in mg/L and as risk levels via the
     rule-based classifier.
  7. Save the model (models/do_forecast.joblib), the scores
     (models/do_forecast_metrics.json) and a chart for the PPT
     (docs/figures/do_forecast.png).
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import joblib
import matplotlib

matplotlib.use("Agg")  # draw charts to files, no window
import matplotlib.dates
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sklearn
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.inspection import permutation_importance
from sklearn.linear_model import Ridge
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from backend.do_features import (FEATURES, HORIZONS_HOURS, STEPS_PER_HOUR,
                                 build_features, to_regular_grid)
from backend.risk_classifier import classify, in_range, load_thresholds

ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = ROOT / "data" / "Ponds data.csv"
MODEL_FILE = ROOT / "models" / "do_forecast.joblib"
METRICS_FILE = ROOT / "models" / "do_forecast_metrics.json"
CHART_FILE = ROOT / "docs" / "figures" / "do_forecast.png"

TRAIN_SHARE, VAL_SHARE = 0.70, 0.15
AVERAGE_WINDOWS = ["do_mean_1h", "do_mean_3h", "do_mean_6h", "do_mean_24h"]

# Chart colours (validated with the dataviz palette checker; see commit notes)
C_ACTUAL, C_PERSIST, C_MODEL = "#c3ccd1", "#5b6b73", "#2a78d6"
C_INK, C_MUTED = "#0f2a36", "#56707b"
BAND = {"danger": "#fdecea", "warning": "#fff3dc", "safe": "#e6f4ea"}  # DESIGN.md status backgrounds


# ---------------------------------------------------------------- 1. load

def load_ponds(thresholds: dict) -> dict[str, pd.DataFrame]:
    """Return {station: DataFrame indexed by time} with clean numeric columns."""
    raw = pd.read_csv(DATA_FILE, low_memory=False).dropna(subset=["station", "Date", "Time"])
    raw["station"] = raw["station"].str.lower()
    raw["ts"] = pd.to_datetime(raw["Date"] + " " + raw["Time"], format="%d-%m-%Y %H:%M:%S", errors="coerce")
    df = pd.DataFrame({
        "station": raw["station"],
        "ts": raw["ts"],
        # errors="coerce" turns spreadsheet junk like "#VALUE!" into NaN
        "dissolved_oxygen": pd.to_numeric(raw["DO"], errors="coerce"),
        "temperature": pd.to_numeric(raw["TEMP"], errors="coerce"),
        "ph": pd.to_numeric(raw["PH"], errors="coerce"),
    }).dropna(subset=["ts"])

    # Same sensor-fault limits as the classifier (config/thresholds.toml).
    for col in ["dissolved_oxygen", "temperature", "ph"]:
        plausible = thresholds[col]["plausible"]
        ok = df[col].apply(lambda v: pd.isna(v) or in_range(v, plausible))
        df.loc[~ok, col] = np.nan

    return {st: g.set_index("ts")[["dissolved_oxygen", "temperature", "ph"]]
            for st, g in df.groupby("station")}


# ---------------------------------------------------------------- 2-3. features + targets

def make_table(ponds: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """One row per (station, time): features + actual future DO for each horizon."""
    parts = []
    for station, readings in ponds.items():
        grid = to_regular_grid(readings)
        feats = build_features(grid)
        for h in HORIZONS_HOURS:
            future = grid["dissolved_oxygen"].shift(-h * STEPS_PER_HOUR)
            feats[f"target_{h}h"] = future.reindex(feats.index)
        feats["station"] = station
        parts.append(feats)
    return pd.concat(parts).rename_axis("ts").reset_index()


def split_by_time(table: pd.DataFrame) -> dict[str, pd.DataFrame]:
    """Chronological split. Rows whose 6 h target would cross into the next period are dropped."""
    times = np.sort(table["ts"].unique())
    t_val = times[int(len(times) * TRAIN_SHARE)]
    t_test = times[int(len(times) * (TRAIN_SHARE + VAL_SHARE))]
    gap = pd.Timedelta(hours=max(HORIZONS_HOURS))
    return {
        "train": table[table["ts"] + gap < t_val],
        "val": table[(table["ts"] >= t_val) & (table["ts"] + gap < t_test)],
        "test": table[table["ts"] >= t_test],
    }


# ---------------------------------------------------------------- 4-5. models

def candidate_models():
    return {
        "linear (Ridge)": make_pipeline(StandardScaler(), Ridge(alpha=1.0)),
        "gradient boosting": HistGradientBoostingRegressor(
            max_iter=200, learning_rate=0.05, max_leaf_nodes=15,
            min_samples_leaf=200, random_state=0),
    }


def mae(pred, actual) -> float:
    return float(np.mean(np.abs(np.asarray(pred) - np.asarray(actual))))


def risk_levels(do_values, thresholds) -> list[str]:
    """DO-only risk level for each value, using the rule-based classifier."""
    return [classify({"dissolved_oxygen": float(v)}, thresholds).level for v in do_values]


# ---------------------------------------------------------------- 6. scoring

def score(pred, actual, thresholds) -> dict:
    pred, actual = np.asarray(pred), np.asarray(actual)
    pred_lvl, true_lvl = np.array(risk_levels(pred, thresholds)), np.array(risk_levels(actual, thresholds))
    unsafe = true_lvl != "safe"
    return {
        "mae_mg_l": round(mae(pred, actual), 3),
        "within_1_mg_l_pct": round(float(np.mean(np.abs(pred - actual) <= 1.0) * 100), 1),
        "risk_level_match_pct": round(float(np.mean(pred_lvl == true_lvl) * 100), 1),
        # Of the moments that really were Warning/Danger, how many did we flag?
        "unsafe_caught_pct": round(float(np.mean(pred_lvl[unsafe] != "safe") * 100), 1) if unsafe.any() else None,
        # Of the moments we flagged, how many really were Warning/Danger?
        "flag_precision_pct": (round(float(np.mean(true_lvl[pred_lvl != "safe"] != "safe") * 100), 1)
                               if (pred_lvl != "safe").any() else None),
    }


# ---------------------------------------------------------------- 7. chart

def draw_chart(test: pd.DataFrame, predictions: dict, results: dict, avg_choice: dict) -> None:
    CHART_FILE.parent.mkdir(parents=True, exist_ok=True)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.6), gridspec_kw={"width_ratios": [2.1, 1]})
    for ax in (ax1, ax2):
        ax.spines[["top", "right"]].set_visible(False)
        ax.spines[["left", "bottom"]].set_color(C_MUTED)
        ax.tick_params(colors=C_MUTED, labelsize=10)
        ax.grid(axis="y", color="#e6eef1", linewidth=0.8)
        ax.set_axisbelow(True)

    # Left: three days of the test period, one pond, 3-hour-ahead forecast.
    h = 3
    station = test["station"].iloc[0]
    rows = test[test["station"] == station].dropna(subset=[f"target_{h}h"])
    start = rows["ts"].iloc[len(rows) // 3]
    window = rows[(rows["ts"] >= start) & (rows["ts"] < start + pd.Timedelta(days=3))]
    idx = window.index
    shown_time = window["ts"] + pd.Timedelta(hours=h)   # plot each forecast at the time it is FOR
    ymax = max(16.0, float(window[f"target_{h}h"].max()) + 1)

    ax1.axhspan(0, 3, color=BAND["danger"], zorder=0)
    ax1.axhspan(3, 5, color=BAND["warning"], zorder=0)
    ax1.axhspan(5, ymax, color=BAND["safe"], zorder=0)
    for y, label in [(1.5, "Danger  < 3"), (4.0, "Warning  3–5"), (ymax - 0.8, "Safe  ≥ 5")]:
        ax1.text(shown_time.iloc[-1], y, label, ha="right", va="center", fontsize=9, color=C_MUTED)

    ax1.plot(shown_time, window[f"target_{h}h"], "o", ms=3.5, color=C_ACTUAL, label="Actual reading")
    ax1.plot(shown_time, predictions["persistence"][h].loc[idx], "--", lw=2, color=C_PERSIST,
             label='Baseline: "DO stays the same"')
    ax1.plot(shown_time, predictions["model"][h].loc[idx], "-", lw=2, color=C_MODEL, label="Model forecast")
    ax1.set_ylim(0, ymax)
    ax1.set_ylabel("Dissolved oxygen (mg/L)", color=C_INK, fontsize=11)
    ax1.set_title(f"3-hours-ahead forecast vs actual — {station}, test period",
                  loc="left", fontsize=12, color=C_INK, fontweight="bold")
    ax1.legend(loc="upper left", frameon=False, fontsize=9.5, ncol=3, labelcolor=C_INK)
    ax1.xaxis.set_major_formatter(matplotlib.dates.DateFormatter("%d %b\n%H:%M"))

    # Right: average error per horizon.
    methods = [("persistence", 'DO stays\nthe same', C_ACTUAL),
               ("recent_average", "Recent\naverage", C_PERSIST),
               ("model", "Model", C_MODEL)]
    x = np.arange(len(HORIZONS_HOURS))
    width = 0.26
    for i, (key, label, colour) in enumerate(methods):
        vals = [results[f"{hh}h"][key]["mae_mg_l"] for hh in HORIZONS_HOURS]
        bars = ax2.bar(x + (i - 1) * width, vals, width - 0.03, color=colour, label=label.replace("\n", " "))
        for b, v in zip(bars, vals):
            ax2.text(b.get_x() + b.get_width() / 2, v + 0.05, f"{v:.1f}", ha="center", va="bottom",
                     fontsize=9, color=C_INK)
    ax2.set_xticks(x, [f"{hh} h ahead" for hh in HORIZONS_HOURS])
    ax2.tick_params(axis="x", labelrotation=0)
    ax2.set_ylabel("Average error (mg/L) — lower is better", color=C_INK, fontsize=11)
    ax2.set_title("Average forecast error, test period", loc="left", fontsize=12, color=C_INK, fontweight="bold")
    ax2.legend(loc="upper center", bbox_to_anchor=(0.5, -0.1), frameon=False, ncol=3, fontsize=9.5,
               labelcolor=C_INK)

    fig.tight_layout()
    fig.savefig(CHART_FILE, dpi=150, facecolor="white")
    plt.close(fig)


# ---------------------------------------------------------------- main

def main() -> None:
    thresholds = load_thresholds()
    print("1. Loading and cleaning Pondsdata ...")
    ponds = load_ponds(thresholds)
    table = make_table(ponds)
    parts = split_by_time(table)
    for name, part in parts.items():
        print(f"   {name:5}: {len(part):6} rows, {part['ts'].min():%d %b %Y} -> {part['ts'].max():%d %b %Y}")

    models, results, predictions, avg_choice, chosen = {}, {}, {"persistence": {}, "model": {}}, {}, {}
    for h in HORIZONS_HOURS:
        target = f"target_{h}h"
        train, val, test = (parts[p].dropna(subset=[target]) for p in ("train", "val", "test"))

        # Best "recent average" window, chosen on validation (fair: it gets tuned too).
        avg_choice[h] = min(AVERAGE_WINDOWS, key=lambda c: mae(val[c], val[target]))

        # Pick the better model on validation.
        val_mae = {}
        for name, model in candidate_models().items():
            model.fit(train[FEATURES], train[target])
            val_mae[name] = mae(model.predict(val[FEATURES]), val[target])
        chosen[h] = min(val_mae, key=val_mae.get)

        # Retrain the winner on train + validation, then score once on test.
        final = candidate_models()[chosen[h]]
        both = pd.concat([train, val])
        final.fit(both[FEATURES], both[target])
        models[h] = final

        pred_model = pd.Series(final.predict(test[FEATURES]), index=test.index)
        pred_persist = test["do_now"]
        pred_avg = test[avg_choice[h]]
        predictions["model"][h] = pred_model
        predictions["persistence"][h] = pred_persist

        results[f"{h}h"] = {
            "persistence": score(pred_persist, test[target], thresholds),
            "recent_average": {**score(pred_avg, test[target], thresholds), "window": avg_choice[h]},
            "model": {**score(pred_model, test[target], thresholds), "type": chosen[h],
                      "validation_mae_mg_l": {k: round(v, 3) for k, v in val_mae.items()}},
            "test_rows": len(test),
        }
        print(f"2. {h} h ahead: chose {chosen[h]} (validation MAE "
              + ", ".join(f"{k} {v:.2f}" for k, v in val_mae.items()) + ")")

    # Which inputs matter most (3 h model): shuffle each feature and see how much worse it gets.
    test3 = parts["test"].dropna(subset=["target_3h"])
    imp = permutation_importance(models[3], test3[FEATURES], test3["target_3h"],
                                 scoring="neg_mean_absolute_error", n_repeats=5, random_state=0)
    importance = {f: round(float(v), 3) for f, v in
                  sorted(zip(FEATURES, imp.importances_mean), key=lambda t: -t[1])}

    # Save model + metrics.
    MODEL_FILE.parent.mkdir(parents=True, exist_ok=True)
    bundle = {
        "models": models,                 # {hours_ahead: fitted sklearn model}
        "features": FEATURES,
        "horizons_hours": HORIZONS_HOURS,
        "trained_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "sklearn_version": sklearn.__version__,
        "test_mae_mg_l": {h: results[f"{h}h"]["model"]["mae_mg_l"] for h in HORIZONS_HOURS},
    }
    joblib.dump(bundle, MODEL_FILE, compress=3)
    metrics = {
        "data": "Kaggle Pondsdata, 'Ponds data.csv', 3 ponds, Feb 2022 – Jan 2023, 20-min readings",
        "split": {name: {"rows": len(p), "from": str(p["ts"].min()), "to": str(p["ts"].max())}
                  for name, p in parts.items()},
        "results": results,
        "feature_importance_3h_mae_increase_mg_l": importance,
    }
    METRICS_FILE.write_text(json.dumps(metrics, indent=2, ensure_ascii=False), encoding="utf-8")
    draw_chart(parts["test"], predictions, results, avg_choice)

    # Plain-language report.
    print("\n3. Test-period results (data the model never saw):")
    for h in HORIZONS_HOURS:
        r = results[f"{h}h"]
        p, a, m = r["persistence"], r["recent_average"], r["model"]
        gain = p["mae_mg_l"] - m["mae_mg_l"]
        print(f"\n   {h} hour(s) ahead ({r['test_rows']} forecasts):")
        print(f"     'DO stays the same' is off by {p['mae_mg_l']:.2f} mg/L on average")
        print(f"     recent average ({a['window']}) is off by {a['mae_mg_l']:.2f} mg/L")
        print(f"     the model ({m['type']}) is off by {m['mae_mg_l']:.2f} mg/L "
              f"-> {gain:.2f} mg/L better than 'stays the same' ({gain / p['mae_mg_l'] * 100:.0f}% less error)")
        print(f"     model within 1 mg/L of the truth {m['within_1_mg_l_pct']}% of the time; "
              f"risk level right {m['risk_level_match_pct']}% "
              f"(baseline {p['risk_level_match_pct']}%)")
        print(f"     real Warning/Danger moments flagged: model {m['unsafe_caught_pct']}%, "
              f"baseline {p['unsafe_caught_pct']}%; flags that were real: model {m['flag_precision_pct']}%, "
              f"baseline {p['flag_precision_pct']}%")
    print("\n4. What the 3 h model relies on most (error increase in mg/L if the input is scrambled):")
    for f, v in list(importance.items())[:5]:
        print(f"     {f:14} {v:+.3f}")
    print(f"\nSaved: {MODEL_FILE.relative_to(ROOT)}, {METRICS_FILE.relative_to(ROOT)}, {CHART_FILE.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
