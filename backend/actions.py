"""
Action checklist for Warning and Danger: step-by-step things the farmer can
do and tick off.

What this file does:
    ACTIONS   every action the app can suggest, in English and Kannada, with
              the sources it is based on (numbers match docs/actions.md).
    PLAN      which actions to show for each problem, e.g. oxygen in Danger.
    checklist(risk) builds the list for one risk result: the actions for each
              cause, most urgent first, without repeats.

Rules for this file (see docs/actions.md):
  - Every action must come from a real source (FAO, TNAU, extension services).
  - No chemical treatments and no doses. Only things like running the aerator,
    changing feed, and adding or draining water.
Kannada text should be reviewed by a native speaker before release.
"""

from __future__ import annotations

# Order = priority: when several problems happen together, the list follows this order.
ACTIONS = {
    "aerator_now": {
        "en": "Run the aerator now. If you have none, splash the water hard with a paddle or stick.",
        "kn": "ಈಗಲೇ ಏರೇಟರ್ ಚಾಲೂ ಮಾಡಿ. ಏರೇಟರ್ ಇಲ್ಲದಿದ್ದರೆ ಹುಟ್ಟು ಅಥವಾ ಕೋಲಿನಿಂದ ನೀರನ್ನು ಜೋರಾಗಿ ಬಡಿಯಿರಿ.",
        "sources": [1, 2, 3],
    },
    "stop_feeding": {
        "en": "Stop feeding until the reading is back to normal.",
        "kn": "ಅಳತೆ ಸಾಮಾನ್ಯ ಸ್ಥಿತಿಗೆ ಬರುವವರೆಗೆ ಆಹಾರ ನೀಡುವುದನ್ನು ನಿಲ್ಲಿಸಿ.",
        "sources": [1, 4],
    },
    "cool_water": {
        "en": "Let in cooler water and drain off the warmest water from the top.",
        "kn": "ತಂಪಾದ ನೀರು ಒಳಗೆ ಬಿಡಿ ಮತ್ತು ಮೇಲಿನ ಬಿಸಿ ನೀರನ್ನು ಹೊರಗೆ ಬಿಡಿ.",
        "sources": [1],
    },
    "fresh_water": {
        "en": "Let in fresh, clean water and drain some of the stale bottom water.",
        "kn": "ಶುದ್ಧ ಹೊಸ ನೀರು ಒಳಗೆ ಬಿಡಿ ಮತ್ತು ತಳದ ಹಳೆಯ ನೀರನ್ನು ಸ್ವಲ್ಪ ಹೊರಗೆ ಬಿಡಿ.",
        "sources": [1],
    },
    "water_change": {
        "en": "Change a quarter to half of the pond water, only if your new water is clean.",
        "kn": "ಹೊಸ ನೀರು ಶುದ್ಧವಾಗಿದ್ದರೆ ಮಾತ್ರ, ಕೊಳದ ಕಾಲು ಭಾಗದಿಂದ ಅರ್ಧದಷ್ಟು ನೀರನ್ನು ಬದಲಾಯಿಸಿ.",
        "sources": [4],
    },
    "aerator_night": {
        "en": "Run the aerator tonight, from late evening until after sunrise.",
        "kn": "ಇಂದು ರಾತ್ರಿ ಸಂಜೆ ತಡವಾಗಿನಿಂದ ಸೂರ್ಯೋದಯದ ನಂತರದವರೆಗೆ ಏರೇಟರ್ ಚಾಲೂ ಇಡಿ.",
        "sources": [2, 3],
    },
    "reduce_feeding": {
        "en": "Give less feed today. Do not overfeed.",
        "kn": "ಇಂದು ಕಡಿಮೆ ಆಹಾರ ನೀಡಿ. ಹೆಚ್ಚು ಆಹಾರ ಹಾಕಬೇಡಿ.",
        "sources": [1, 4, 5],
    },
    "no_fertiliser": {
        "en": "Do not add fertiliser or manure for now.",
        "kn": "ಸದ್ಯಕ್ಕೆ ಗೊಬ್ಬರ ಅಥವಾ ಸಗಣಿ ಹಾಕಬೇಡಿ.",
        "sources": [4, 5],
    },
    "watch_fish": {
        "en": "Watch for fish gasping at the surface, especially before sunrise.",
        "kn": "ಮೀನುಗಳು ಮೇಲ್ಮೈಗೆ ಬಂದು ಗಾಳಿಗಾಗಿ ಒದ್ದಾಡುತ್ತಿವೆಯೇ ನೋಡಿ, ವಿಶೇಷವಾಗಿ ಸೂರ್ಯೋದಯದ ಮೊದಲು.",
        "sources": [1, 2],
    },
    "retest_oxygen_evening": {
        "en": "Test oxygen again late this evening (8–10 pm) to see if it will fall too low at night.",
        "kn": "ರಾತ್ರಿ ಆಮ್ಲಜನಕ ತುಂಬಾ ಕಡಿಮೆಯಾಗುತ್ತದೆಯೇ ಎಂದು ತಿಳಿಯಲು ಇಂದು ರಾತ್ರಿ 8–10 ಗಂಟೆಗೆ ಮತ್ತೆ ಪರೀಕ್ಷಿಸಿ.",
        "sources": [2],
    },
    "retest_ph_morning": {
        "en": "Test pH again early tomorrow morning. pH is highest in the afternoon and falls by morning.",
        "kn": "ನಾಳೆ ಬೆಳಿಗ್ಗೆ ಬೇಗ pH ಮತ್ತೆ ಪರೀಕ್ಷಿಸಿ. ಮಧ್ಯಾಹ್ನ pH ಅತಿ ಹೆಚ್ಚಿರುತ್ತದೆ, ಬೆಳಿಗ್ಗೆಗೆ ಕಡಿಮೆಯಾಗುತ್ತದೆ.",
        "sources": [5],
    },
    "retest_ph_afternoon": {
        "en": "Test pH again this afternoon. pH is lowest in the early morning and rises during the day.",
        "kn": "ಇಂದು ಮಧ್ಯಾಹ್ನ pH ಮತ್ತೆ ಪರೀಕ್ಷಿಸಿ. ಬೆಳಿಗ್ಗೆ pH ಅತಿ ಕಡಿಮೆ ಇರುತ್ತದೆ, ಹಗಲಿನಲ್ಲಿ ಏರುತ್ತದೆ.",
        "sources": [5],
    },
}

# (parameter, direction, level) -> actions. A problem missing here gets no checklist,
# because no source gave a non-chemical action for it (e.g. cold water).
PLAN = {
    ("dissolved_oxygen", "low", "warning"): ["aerator_night", "reduce_feeding", "retest_oxygen_evening", "watch_fish"],
    ("dissolved_oxygen", "low", "danger"):  ["aerator_now", "stop_feeding", "fresh_water", "watch_fish"],
    ("temperature", "high", "warning"):     ["cool_water", "retest_oxygen_evening"],
    ("temperature", "high", "danger"):      ["cool_water", "aerator_now", "watch_fish"],
    ("ammonia", "high", "warning"):         ["reduce_feeding", "no_fertiliser", "aerator_night"],
    ("ammonia", "high", "danger"):          ["stop_feeding", "water_change", "no_fertiliser", "aerator_now"],
    ("ph", "high", "warning"):              ["retest_ph_morning", "no_fertiliser", "reduce_feeding"],
    ("ph", "high", "danger"):               ["retest_ph_morning", "no_fertiliser", "reduce_feeding"],
    ("ph", "low", "warning"):               ["retest_ph_afternoon"],
    ("ph", "low", "danger"):                ["retest_ph_afternoon"],
    ("nitrate", "high", "warning"):         ["reduce_feeding", "water_change"],
}

PRIORITY = list(ACTIONS)


def checklist(risk: dict) -> list[dict]:
    """
    Actions for a risk result (the dictionary from RiskResult.to_dict()).
    Empty when the pond is Safe or Unknown. Each item: {"id", "en", "kn", "sources"}.
    """
    if risk["level"] not in ("warning", "danger"):
        return []
    causes = [p for p in risk["parameters"] if p["parameter"] in risk["causes"]]
    ids = {a for p in causes for a in PLAN.get((p["parameter"], p["direction"], p["level"]), [])}
    return [{"id": a, **ACTIONS[a]} for a in PRIORITY if a in ids]
