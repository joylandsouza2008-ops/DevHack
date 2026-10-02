# Pond health score (0–100)

The big ring on the dashboard shows one number from 0 (very bad) to 100 (very
good). Code: `backend/health_score.py`. Tests: `tests/test_health_score.py`.

The score is a **summary of the Safe / Warning / Danger status**, not a new
prediction. It uses the same graded readings as the status banner, and adds no
new thresholds of its own (apart from the oxygen "headroom" below).

## Rule 1: the score never contradicts the status

Each status owns its own range. The score can never leave it.

| Status  | Score range |
|---------|-------------|
| Safe    | 75 – 100    |
| Warning | 40 – 74     |
| Danger  | 0 – 39      |
| Unknown (no usable readings) | no score, ring is empty and shows "-" |

So a Danger pond can never show a "good" number, and a Safe pond can never
show a "bad" one. A final safety net in the code clamps the result into the
range in case of any rounding.

## Rule 2: inside the range, show how close to the edge the pond is

**Safe:** `75 + 25 × oxygen headroom`

- oxygen headroom = (DO − 5) ÷ 2, kept between 0 and 1
- DO 5.0 mg/L (just at the Safe limit) → 75; DO 6.0 → 88; DO 7.0 or more → 100
- No DO reading → 100

Dissolved oxygen is used because it changes fastest (it falls every night)
and is the most common cause of sudden fish kills. A Safe pond whose oxygen is
sliding towards 5 mg/L shows a lower Safe score, an early hint before the
status changes.

**Warning:** `40 + 34 × (share of checked readings that are Safe)`

- 1 reading in Warning, 3 Safe → 40 + 34 × 3/4 = 65.5 → **66**
- 2 in Warning, 2 Safe → 40 + 34 × 2/4 → **57**

**Danger:** `39 × (average points)`, where each checked reading scores
Safe = 1, Warning = 0.5, Danger = 0

- DO in Danger, pH / temperature / ammonia Safe → 39 × 3/4 = 29.25 → **29**
- DO in Danger, pH in Warning, 2 Safe → 39 × 2.5/4 → **24**

More problem readings = lower score. "Checked readings" are the graded ones
(DO, pH, temperature, ammonia, nitrate). Turbidity is information only and
ammonia without pH and temperature cannot be graded, so neither counts.
Impossible readings (sensor faults) are left out.

The numbers are rounded to whole numbers.

## What the score is NOT

- Not a measured value, and not a probability of fish death.
- Not trained on data, so it has no "accuracy". On the dashboard it is
  worked out from the **simulated** readings, so the card carries the
  "Simulated data / ಅನುಕರಿಸಿದ (ಸಿಮ್ಯುಲೇಟೆಡ್) ಡೇಟಾ" tag.
- The range boundaries (75 / 40) and the 2 mg/L headroom are our judgement,
  picked so the three ranges are easy to tell apart on the ring.
