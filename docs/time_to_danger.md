# "Time until danger" — method and results

This is what the farmer-facing app shows instead of the DO forecast. The forecast's typical error (±4.5 mg/L, see [do_forecast.md](do_forecast.md)) is wider than the whole Warning band (3–5 mg/L), so it is kept here in `docs/` as an experiment and is **not** shown in the app.

## What it does

If dissolved oxygen (DO) has been falling over the last 1–2 hours, it estimates when DO will reach the **Danger level (3 mg/L)** and says so in plain words:

> **English:** Oxygen is falling (about 1.2 mg/L per hour). At this rate it may reach the danger level (3 mg/L) in about 2 hours, around 03:10. Get the aerator ready now.
>
> **ಕನ್ನಡ:** ಆಮ್ಲಜನಕ ಕಡಿಮೆಯಾಗುತ್ತಿದೆ (ಗಂಟೆಗೆ ಸುಮಾರು 1.2 mg/L). ಇದೇ ವೇಗದಲ್ಲಿ ಸುಮಾರು 2 ಗಂಟೆಗಳಲ್ಲಿ (03:10 ಹೊತ್ತಿಗೆ) ಅಪಾಯದ ಮಟ್ಟ (3 mg/L) ತಲುಪಬಹುದು. ಈಗಲೇ ಏರೇಟರ್ ಸಿದ್ಧಪಡಿಸಿ.

## How it works

1. Take the DO readings from the last **2 hours** (at least 4 readings covering at least 1 hour).
2. Fit a straight line through them. The slope is how fast DO is changing (mg/L per hour).
3. Check that the readings really follow the line (R² ≥ 0.6; 1 = perfectly straight, 0 = no pattern). Random jumps from sensor noise don't count as a fall.
4. If DO is falling faster than **0.3 mg/L per hour**, extend the line to 3 mg/L. Report it only if that's within **6 hours**. The time is shown rounded to 10 minutes, because it's an estimate.

All settings live in `config/thresholds.toml` under `[time_to_danger]` (our judgement, not from a source). Code: `backend/time_to_danger.py`.

## Check 1 — simulated night oxygen crash (demo check, simulated data)

This shows that the feature behaves as designed. It is **not** an accuracy result, because the data is simulated.

| Simulated time | DO (mg/L) | Pond status | Time until danger says |
|---|---|---|---|
| 21:20 | 11.3 | Safe | danger expected around 01:50 (first alert) |
| 23:20 | 7.6 | Safe | around 01:30 |
| 01:20 | 5.1 | Warning | **about 2 hours, around 03:10** |
| 02:40 | 3.9 | Warning | about 30 minutes, around 03:10 |
| **03:20** | **2.96** | **Danger** | already at the danger level |

The first alert comes **6 hours before** DO actually falls below 3 mg/L, while the pond still reads Safe. The estimated time gets more accurate as the night goes on. Screenshots: [`screenshots/`](screenshots/).

## Check 2 — real Pondsdata readings: would it have warned correctly?

We replayed every pond's real readings in time order and ran the estimate at each 20-minute step, giving it only the readings up to that moment, as the live app would. Script: `python -m ml.evaluate_time_to_danger`. Numbers: [`time_to_danger_eval.json`](time_to_danger_eval.json).

| On real Pondsdata (72,435 moments, 3 ponds) | Without the R² check | **With it (used)** |
|---|---|---|
| Alerts per pond per day | 9.3 | **1.7** |
| Alerts followed by real danger within 6 h | 1.4 % | **1.0 %** |
| Chance level (from a random moment) | 1.6 % | 1.6 % |
| Alerts within ±1 h of the real time | 0.5 % | 0.2 % |
| Real danger events caught in advance (of 71) | 100 %* | 26.8 % |

\* Only because it alerted constantly, so it means nothing.

**In plain words: on the real Pondsdata readings, the estimate is no better than chance.** An alert is followed by real danger about 1 time in 100, no more often than from a random moment.

**Why:** in this dataset, readings below 3 mg/L are isolated noise blips. After a low reading, the next one is also low only 5% of the time, and there are no gradual night-time declines. A trend-based warning needs a trend, and this data has none. The R² check removes 80% of the false alarms caused by noise; the remaining 1.7 per pond per day are still noise.

**What this means for the project:**
- The feature works on smooth, gradual oxygen declines (the simulated crash), which is how real pond oxygen crashes typically develop.
- We could **not** validate it on real data, because the public dataset has no real crashes, only sensor noise.
- Before real use it must be checked against real sensor data with genuine night-time oxygen declines.
