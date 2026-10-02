"""
Farmer-facing text for risk results, in English ("en") and Kannada ("kn").

This file holds words only, no rules or numbers. The classifier picks a
message by (parameter, direction, level) and fills in {value} and {unit}.

    direction = "low"  -> the reading is below the safe range
    direction = "high" -> the reading is above the safe range

Keep sentences short: what is wrong, why it matters, what to do.
Kannada text should be reviewed by a native speaker before release.
"""

LEVEL_NAMES = {
    "safe":    {"en": "Safe",    "kn": "ಸುರಕ್ಷಿತ"},
    "warning": {"en": "Warning", "kn": "ಎಚ್ಚರಿಕೆ"},
    "danger":  {"en": "Danger",  "kn": "ಅಪಾಯ"},
    "unknown": {"en": "Unknown", "kn": "ತಿಳಿದಿಲ್ಲ"},
}

PARAMETER_NAMES = {
    "dissolved_oxygen": {"en": "Dissolved oxygen", "kn": "ಕರಗಿದ ಆಮ್ಲಜನಕ"},
    "ph":               {"en": "pH",               "kn": "ಪಿಎಚ್ (pH)"},
    "temperature":      {"en": "Water temperature", "kn": "ನೀರಿನ ತಾಪಮಾನ"},
    "ammonia":          {"en": "Ammonia",          "kn": "ಅಮೋನಿಯಾ"},
    "nitrate":          {"en": "Nitrate",          "kn": "ನೈಟ್ರೇಟ್"},
    "turbidity":        {"en": "Turbidity",        "kn": "ನೀರಿನ ಮಬ್ಬು (ಟರ್ಬಿಡಿಟಿ)"},
}

# (parameter, direction, level) -> message
REASONS = {
    ("dissolved_oxygen", "low", "warning"): {
        "en": "Oxygen is low ({value} {unit}). Fish may stop eating. Run the aerator.",
        "kn": "ಆಮ್ಲಜನಕ ಕಡಿಮೆ ಇದೆ ({value} {unit}). ಮೀನುಗಳು ಆಹಾರ ತಿನ್ನುವುದನ್ನು ನಿಲ್ಲಿಸಬಹುದು. ಏರೇಟರ್ ಚಾಲೂ ಮಾಡಿ.",
    },
    ("dissolved_oxygen", "low", "danger"): {
        "en": "Oxygen is very low ({value} {unit}). Fish can die. Turn on the aerator now and add fresh water.",
        "kn": "ಆಮ್ಲಜನಕ ತುಂಬಾ ಕಡಿಮೆ ಇದೆ ({value} {unit}). ಮೀನುಗಳು ಸಾಯಬಹುದು. ತಕ್ಷಣ ಏರೇಟರ್ ಚಾಲೂ ಮಾಡಿ ಮತ್ತು ಹೊಸ ನೀರು ಹಾಕಿ.",
    },
    ("ph", "low", "warning"): {
        "en": "Water is acidic (pH {value}). Fish grow slowly. Ask your fisheries officer about adding lime.",
        "kn": "ನೀರು ಆಮ್ಲೀಯವಾಗಿದೆ (pH {value}). ಮೀನುಗಳು ನಿಧಾನವಾಗಿ ಬೆಳೆಯುತ್ತವೆ. ಸುಣ್ಣ ಹಾಕುವ ಬಗ್ಗೆ ಮೀನುಗಾರಿಕೆ ಅಧಿಕಾರಿಯನ್ನು ಕೇಳಿ.",
    },
    ("ph", "low", "danger"): {
        "en": "Water is very acidic (pH {value}). Fish can die. Add fresh water and contact your fisheries officer today.",
        "kn": "ನೀರು ತುಂಬಾ ಆಮ್ಲೀಯವಾಗಿದೆ (pH {value}). ಮೀನುಗಳು ಸಾಯಬಹುದು. ಹೊಸ ನೀರು ಹಾಕಿ ಮತ್ತು ಇಂದೇ ಮೀನುಗಾರಿಕೆ ಅಧಿಕಾರಿಯನ್ನು ಸಂಪರ್ಕಿಸಿ.",
    },
    ("ph", "high", "warning"): {
        "en": "Water is alkaline (pH {value}). Ammonia becomes more harmful. Add fresh water and stop adding fertiliser.",
        "kn": "ನೀರು ಕ್ಷಾರೀಯವಾಗಿದೆ (pH {value}). ಅಮೋನಿಯಾ ಹೆಚ್ಚು ಹಾನಿಕಾರಕವಾಗುತ್ತದೆ. ಹೊಸ ನೀರು ಹಾಕಿ ಮತ್ತು ಗೊಬ್ಬರ ಹಾಕುವುದನ್ನು ನಿಲ್ಲಿಸಿ.",
    },
    ("ph", "high", "danger"): {
        "en": "Water is very alkaline (pH {value}). Fish can die. Add fresh water now and contact your fisheries officer.",
        "kn": "ನೀರು ತುಂಬಾ ಕ್ಷಾರೀಯವಾಗಿದೆ (pH {value}). ಮೀನುಗಳು ಸಾಯಬಹುದು. ತಕ್ಷಣ ಹೊಸ ನೀರು ಹಾಕಿ ಮತ್ತು ಮೀನುಗಾರಿಕೆ ಅಧಿಕಾರಿಯನ್ನು ಸಂಪರ್ಕಿಸಿ.",
    },
    ("temperature", "low", "warning"): {
        "en": "Water is cool ({value} {unit}). Fish eat less. Reduce the feed.",
        "kn": "ನೀರು ತಣ್ಣಗಿದೆ ({value} {unit}). ಮೀನುಗಳು ಕಡಿಮೆ ತಿನ್ನುತ್ತವೆ. ಆಹಾರ ಕಡಿಮೆ ಮಾಡಿ.",
    },
    ("temperature", "low", "danger"): {
        "en": "Water is too cold ({value} {unit}). Fish are stressed and may fall sick. Feed very little.",
        "kn": "ನೀರು ತುಂಬಾ ತಣ್ಣಗಿದೆ ({value} {unit}). ಮೀನುಗಳಿಗೆ ಒತ್ತಡ ಉಂಟಾಗಿ ರೋಗ ಬರಬಹುದು. ತುಂಬಾ ಕಡಿಮೆ ಆಹಾರ ನೀಡಿ.",
    },
    ("temperature", "high", "warning"): {
        "en": "Water is warm ({value} {unit}). Oxygen will drop. Run the aerator and add fresh water.",
        "kn": "ನೀರು ಬಿಸಿಯಾಗಿದೆ ({value} {unit}). ಆಮ್ಲಜನಕ ಕಡಿಮೆಯಾಗುತ್ತದೆ. ಏರೇಟರ್ ಚಾಲೂ ಮಾಡಿ ಮತ್ತು ಹೊಸ ನೀರು ಹಾಕಿ.",
    },
    ("temperature", "high", "danger"): {
        "en": "Water is too hot ({value} {unit}). Fish can die. Add fresh water now, run the aerator and stop feeding.",
        "kn": "ನೀರು ತುಂಬಾ ಬಿಸಿಯಾಗಿದೆ ({value} {unit}). ಮೀನುಗಳು ಸಾಯಬಹುದು. ತಕ್ಷಣ ಹೊಸ ನೀರು ಹಾಕಿ, ಏರೇಟರ್ ಚಾಲೂ ಮಾಡಿ ಮತ್ತು ಆಹಾರ ನಿಲ್ಲಿಸಿ.",
    },
    ("ammonia", "high", "warning"): {
        "en": "Harmful ammonia is rising ({value} {unit}). Reduce the feed and add fresh water.",
        "kn": "ಹಾನಿಕಾರಕ ಅಮೋನಿಯಾ ಹೆಚ್ಚುತ್ತಿದೆ ({value} {unit}). ಆಹಾರ ಕಡಿಮೆ ಮಾಡಿ ಮತ್ತು ಹೊಸ ನೀರು ಹಾಕಿ.",
    },
    ("ammonia", "high", "danger"): {
        "en": "Harmful ammonia is very high ({value} {unit}). Fish can die. Stop feeding today and add fresh water.",
        "kn": "ಹಾನಿಕಾರಕ ಅಮೋನಿಯಾ ತುಂಬಾ ಹೆಚ್ಚಾಗಿದೆ ({value} {unit}). ಮೀನುಗಳು ಸಾಯಬಹುದು. ಇಂದು ಆಹಾರ ನೀಡುವುದನ್ನು ನಿಲ್ಲಿಸಿ ಮತ್ತು ಹೊಸ ನೀರು ಹಾಕಿ.",
    },
    ("nitrate", "high", "warning"): {
        "en": "Nitrate is high ({value} {unit}). Change some of the water and reduce the feed.",
        "kn": "ನೈಟ್ರೇಟ್ ಹೆಚ್ಚಾಗಿದೆ ({value} {unit}). ಸ್ವಲ್ಪ ನೀರು ಬದಲಾಯಿಸಿ ಮತ್ತು ಆಹಾರ ಕಡಿಮೆ ಮಾಡಿ.",
    },
}

ALL_SAFE = {
    "en": "All readings are in the safe range.",
    "kn": "ಎಲ್ಲಾ ಅಳತೆಗಳು ಸುರಕ್ಷಿತ ಮಟ್ಟದಲ್ಲಿವೆ.",
}

SENSOR_ERROR = {
    "en": "{name} reading looks wrong ({value}). Check the sensor.",
    "kn": "{name} ಅಳತೆ ತಪ್ಪಾಗಿರುವಂತೆ ಕಾಣುತ್ತಿದೆ ({value}). ಸೆನ್ಸರ್ ಪರಿಶೀಲಿಸಿ.",
}

AMMONIA_NEEDS_PH_AND_TEMPERATURE = {
    "en": "Ammonia could not be checked because pH or temperature is missing.",
    "kn": "pH ಅಥವಾ ತಾಪಮಾನ ಇಲ್ಲದ ಕಾರಣ ಅಮೋನಿಯಾ ಪರಿಶೀಲಿಸಲು ಆಗಲಿಲ್ಲ.",
}

# --- Time until danger (backend/time_to_danger.py) -----------------------
# {rate} mg/L per hour, {duration}/{duration_kn} e.g. "about 2 hours",
# {clock} e.g. "03:20", {danger} the danger level, {hours} the look-ahead limit.
TIME_TO_DANGER = {
    "danger_expected": {
        "en": "Oxygen is falling (about {rate} mg/L per hour). At this rate it may reach the danger "
              "level ({danger} mg/L) in {duration}, around {clock}. Get the aerator ready now.",
        "kn": "ಆಮ್ಲಜನಕ ಕಡಿಮೆಯಾಗುತ್ತಿದೆ (ಗಂಟೆಗೆ ಸುಮಾರು {rate} mg/L). ಇದೇ ವೇಗದಲ್ಲಿ {duration_kn} "
              "({clock} ಹೊತ್ತಿಗೆ) ಅಪಾಯದ ಮಟ್ಟ ({danger} mg/L) ತಲುಪಬಹುದು. ಈಗಲೇ ಏರೇಟರ್ ಸಿದ್ಧಪಡಿಸಿ.",
    },
    "already_danger": {
        "en": "Oxygen is already at the danger level.",
        "kn": "ಆಮ್ಲಜನಕ ಈಗಾಗಲೇ ಅಪಾಯದ ಮಟ್ಟದಲ್ಲಿದೆ.",
    },
    "falling_slowly": {
        "en": "Oxygen is falling slowly. No danger expected in the next {hours} hours.",
        "kn": "ಆಮ್ಲಜನಕ ನಿಧಾನವಾಗಿ ಕಡಿಮೆಯಾಗುತ್ತಿದೆ. ಮುಂದಿನ {hours} ಗಂಟೆಗಳಲ್ಲಿ ಅಪಾಯ ನಿರೀಕ್ಷಿಸಿಲ್ಲ.",
    },
    "not_falling": {
        "en": "Oxygen is not falling.",
        "kn": "ಆಮ್ಲಜನಕ ಕಡಿಮೆಯಾಗುತ್ತಿಲ್ಲ.",
    },
    "not_enough_data": {
        "en": "Not enough recent oxygen readings to estimate.",
        "kn": "ಅಂದಾಜು ಮಾಡಲು ಇತ್ತೀಚಿನ ಆಮ್ಲಜನಕ ಅಳತೆಗಳು ಸಾಕಷ್ಟಿಲ್ಲ.",
    },
}

NO_VALID_READINGS = {
    "en": "No valid readings. Check the sensors.",
    "kn": "ಸರಿಯಾದ ಅಳತೆಗಳು ಇಲ್ಲ. ಸೆನ್ಸರ್‌ಗಳನ್ನು ಪರಿಶೀಲಿಸಿ.",
}
