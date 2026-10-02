"""
Check the "time until danger" estimate on REAL Pondsdata readings (never
simulated data): how often would it have given a correct early warning?

Run from the project folder:
    python -m ml.evaluate_time_to_danger

Method: replay every pond's readings in time order. At each 20-minute step,
give the estimator only the readings up to that moment (like the live app),
then look at what really happened next.

  Alert            = the estimator says "danger expected" within 6 hours.
  Correct alert    = DO really dropped below 3 mg/L within the next 6 hours.
  Well-timed alert = ... and the real drop came within ±1 hour of the estimate.
  Chance level     = how often DO drops below 3 mg/L within 6 hours from a
                     random moment. An alert is only useful if it is right
                     clearly more often than this.
  Danger event     = DO drops below 3 mg/L after 2 hours of readings above it.
  Caught event     = an alert was shown at least 20 minutes before the event.

Results: printed, saved to docs/time_to_danger_eval.json, written up in
docs/time_to_danger.md.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

from backend.do_features import STEPS_PER_HOUR, to_regular_grid
from backend.risk_classifier import load_thresholds
from backend.simulator import reject_simulated
from backend.time_to_danger import estimate_time_to_danger
from ml.train_do_forecast import load_ponds

ROOT = Path(__file__).resolve().parent.parent
RESULTS_FILE = ROOT / "docs" / "time_to_danger_eval.json"
TIMING_TOLERANCE_HOURS = 1.0


def replay_pond(do: pd.Series, thresholds: dict) -> pd.DataFrame:
    """Run the estimator at every step, using only readings up to that step."""
    cfg = thresholds["time_to_danger"]
    danger = thresholds["dissolved_oxygen"]["warning"]["min"]
    look_back = int(cfg["window_hours"] * STEPS_PER_HOUR)
    ahead = int(cfg["max_hours_ahead"] * STEPS_PER_HOUR)
    values, times = do.to_numpy(), do.index

    # When does DO next drop below the danger level, looking forward from each step?
    below = values < danger
    next_below = np.full(len(values), np.nan)
    upcoming = np.nan
    for i in range(len(values) - 1, -1, -1):
        next_below[i] = upcoming
        if below[i]:
            upcoming = i

    rows = []
    for i in range(look_back, len(values) - ahead):
        if np.isnan(values[i]) or values[i] < danger:
            continue                      # only judge moments that are currently above Danger
        est = estimate_time_to_danger(do.iloc[i - look_back:i + 1], thresholds)
        steps_to_real = next_below[i] - i if not np.isnan(next_below[i]) else np.inf
        rows.append({
            "time": times[i],
            "status": est["status"],
            "estimated_hours": est["hours_to_danger"],
            "real_hours": steps_to_real / STEPS_PER_HOUR,
        })
    return pd.DataFrame(rows)


def danger_events(do: pd.Series, danger: float) -> list[pd.Timestamp]:
    """Times DO first drops below danger after >= 2 h of valid readings at or above it."""
    events, need = [], 2 * STEPS_PER_HOUR
    values = do.to_numpy()
    for i in range(need, len(values)):
        before = values[i - need:i]
        if values[i] < danger and np.all(before[~np.isnan(before)] >= danger) and (~np.isnan(before)).sum() >= 4:
            events.append(do.index[i])
    return events


def main() -> None:
    thresholds = load_thresholds()
    cfg = thresholds["time_to_danger"]
    danger = thresholds["dissolved_oxygen"]["warning"]["min"]
    horizon = cfg["max_hours_ahead"]

    replays, caught, lead_times, n_events = [], 0, [], 0
    for station, readings in load_ponds(thresholds).items():
        reject_simulated(readings)
        do = to_regular_grid(readings)["dissolved_oxygen"]
        replay = replay_pond(do, thresholds)
        replay["station"] = station
        replays.append(replay)

        alert_times = replay.loc[replay["status"] == "danger_expected", "time"]
        for event in danger_events(do, danger):
            if event < do.index[0] + pd.Timedelta(hours=horizon):
                continue
            n_events += 1
            window = alert_times[(alert_times >= event - pd.Timedelta(hours=horizon))
                                 & (alert_times <= event - pd.Timedelta(minutes=20))]
            if len(window):
                caught += 1
                lead_times.append((event - window.min()) / pd.Timedelta(hours=1))
        print(f"  {station}: {len(replay)} moments checked")

    r = pd.concat(replays, ignore_index=True)
    alerts = r[r["status"] == "danger_expected"]
    real_within = alerts["real_hours"] <= horizon
    well_timed = (alerts["real_hours"] - alerts["estimated_hours"]).abs() <= TIMING_TOLERANCE_HOURS
    chance = float((r["real_hours"] <= horizon).mean())
    days = (r["time"].max() - r["time"].min()) / pd.Timedelta(days=1)

    # Alert "episodes": consecutive alert steps for a pond count as one alert to the farmer.
    episodes = 0
    for _, g in r.groupby("station"):
        on = (g["status"] == "danger_expected").astype(int)
        episodes += int(((on.diff() == 1) | ((on == 1) & (on.index == g.index[0]))).sum())

    results = {
        "data": "Kaggle Pondsdata, 'Ponds data.csv' (real readings only)",
        "settings": cfg | {"danger_level_mg_l": danger, "timing_tolerance_hours": TIMING_TOLERANCE_HOURS},
        "moments_checked": len(r),
        "status_share_pct": (r["status"].value_counts(normalize=True) * 100).round(1).to_dict(),
        "alerts": len(alerts),
        "alert_episodes": episodes,
        "alert_episodes_per_pond_per_day": round(episodes / 3 / days, 1),
        "alerts_correct_pct": round(float(real_within.mean() * 100), 1),
        "alerts_well_timed_pct": round(float(well_timed.mean() * 100), 1),
        "chance_level_pct": round(chance * 100, 1),
        "danger_events": n_events,
        "danger_events_caught_pct": round(caught / n_events * 100, 1) if n_events else None,
        "median_lead_time_hours": round(float(np.median(lead_times)), 2) if lead_times else None,
    }
    RESULTS_FILE.write_text(json.dumps(results, indent=2), encoding="utf-8")

    print("\nOn real Pondsdata readings:")
    print(f"  moments checked: {results['moments_checked']} (DO above {danger:g} mg/L at that moment)")
    print(f"  status share: {results['status_share_pct']}")
    print(f"  alerts: {results['alerts']} steps = {episodes} separate alerts "
          f"(~{results['alert_episodes_per_pond_per_day']} per pond per day)")
    print(f"  alerts followed by real danger within {horizon:g} h: {results['alerts_correct_pct']}% "
          f"(chance level from a random moment: {results['chance_level_pct']}%)")
    print(f"  alerts within ±{TIMING_TOLERANCE_HOURS:g} h of the real time: {results['alerts_well_timed_pct']}%")
    print(f"  real danger events: {n_events}, caught in advance: {results['danger_events_caught_pct']}%, "
          f"median warning time: {results['median_lead_time_hours']} h")
    print(f"\nSaved: {RESULTS_FILE.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
