"""
Pond health score: one number from 0 (very bad) to 100 (very good), shown as
the big ring on the dashboard.

The score can NEVER disagree with the Safe / Warning / Danger status, because
each status owns its own range of scores:

    Safe     75 – 100
    Warning  40 – 74
    Danger    0 – 39

Inside that range the score only moves a little, to show "how close to the
edge" the pond is:

  Safe:    75 + 25 x oxygen headroom
           oxygen headroom = (DO - 5) / 2, kept between 0 and 1
           (DO 5 mg/L -> 75, DO 7 mg/L or more -> 100). Oxygen is used because
           it changes fastest and kills fish quickest. No DO reading -> 100.
  Warning: 40 + 34 x (share of checked readings that are Safe)
  Danger:  39 x (average points of checked readings: Safe 1, Warning 0.5, Danger 0)

So a pond with ONE problem reading scores higher than a pond with three.
Unknown status (no usable readings) -> no score (None).

Full explanation with examples: docs/health_score.md

Example:
    from backend.risk_classifier import classify
    from backend.health_score import health_score
    health_score(classify({"dissolved_oxygen": 2.5, "ph": 7.2}).to_dict())   # 19
"""

from __future__ import annotations

# Score range for each status (lowest, highest). Shared with the docs and tests.
BANDS = {"safe": (75, 100), "warning": (40, 74), "danger": (0, 39)}

DO_SAFE_MIN = 5.0        # mg/L, same as dissolved_oxygen.safe.min in config/thresholds.toml
DO_HEADROOM = 2.0        # mg/L above the Safe limit that counts as "full marks"
POINTS = {"safe": 1.0, "warning": 0.5, "danger": 0.0}


def health_score(risk: dict) -> int | None:
    """
    risk  the dictionary from RiskResult.to_dict() (needs "level" and "parameters").
    Returns a whole number 0–100, or None when the status is unknown.
    """
    level = risk["level"]
    if level not in BANDS:
        return None
    low, high = BANDS[level]
    checked = [p for p in risk["parameters"] if p["level"] in POINTS]

    if level == "safe":
        do = next((p["value"] for p in checked if p["parameter"] == "dissolved_oxygen"), None)
        headroom = 1.0 if do is None else min(1.0, max(0.0, (do - DO_SAFE_MIN) / DO_HEADROOM))
        score = low + (high - low) * headroom
    elif level == "warning":
        share_safe = sum(p["level"] == "safe" for p in checked) / len(checked)
        score = low + (high - low) * share_safe
    else:
        average = sum(POINTS[p["level"]] for p in checked) / len(checked)
        score = high * average

    # Safety net: whatever happens above, stay inside the status's own range.
    return int(min(high, max(low, round(score))))
