"""
Pond care basics for the "Ask AquaNexus" assistant: everyday questions like
"When should I clean the pond?" or "How much should I feed?".

Rules for this file (sources and checks in docs/pond-care.md):
  - Plain words only. NO chemical names, medicines, liming or amounts of anything.
    Those always go to "ask your fisheries officer or KVK" (OFFICER_NOTE).
  - Every sentence comes from a source listed in docs/pond-care.md.

What this file does:
    TOPICS             cleaning, water change, feeding, aerators, daily/weekly checks, stocking:
                       the words that point to each topic and its ready answer (English + Kannada).
    classify(question) which topic a question is about, or None. Understands similar words:
                       tank / pond / kere / ಕೆರೆ, clean / wash, change water ...
    answer(topic, q)   the ready answer in both languages: {"en": ..., "kn": ...}.
    content_lines()    the same facts as plain text, for the AI's content.
Kannada text should be reviewed by a native speaker before release.
"""

from __future__ import annotations

import re

OFFICER_NOTE = {"en": "For liming, chemicals, medicines or amounts of anything, ask your fisheries officer or KVK.",
                "kn": "ಸುಣ್ಣ ಹಾಕುವುದು, ರಾಸಾಯನಿಕಗಳು, ಔಷಧಿಗಳು ಅಥವಾ ಯಾವುದರ ಪ್ರಮಾಣಕ್ಕಾಗಿ ನಿಮ್ಮ ಮೀನುಗಾರಿಕೆ ಅಧಿಕಾರಿ ಅಥವಾ "
                      "KVK ಅನ್ನು ಕೇಳಿ."}

# A tank and a pond are cared for a bit differently (see "cleaning").
TANK_WORDS = re.compile(r"\btanks?\b|ಟ್ಯಾಂಕ್|ತೊಟ್ಟಿ", re.I)

# Each topic: the words that point to it (English, Kannada and Kannada typed in English letters),
# and its ready answer as short sentences. Checked in this order: "change the water" is a water
# question even though "clean" may appear too.
TOPICS = {
    "water_change": {
        "words": re.compile(
            r"\b(change|chang|exchang|replac|renew|refresh|top\s*up|add|new|fresh)\w*\s+(\w+\s+){0,3}water\b"
            r"|\bwater\s+(change|exchange)|neeru\s+badal"
            r"|ನೀರ\S*\s+(\S+\s+){0,3}ಬದಲ|ಹೊಸ\s*ನೀರು|ತಾಜಾ\s*ನೀರು", re.I),
        "title": {"en": "Changing water", "kn": "ನೀರು ಬದಲಾಯಿಸುವುದು"},
        "text": {
            "en": ["Change part of the water, not all of it, when the water smells bad, is very green, "
                   "or oxygen is low (fish gasp at the surface at dawn).",
                   "Let some water out and fill in clean water.",
                   "Don't empty the pond while the fish are in it."],
            "kn": ["ನೀರು ಕೆಟ್ಟ ವಾಸನೆ ಬಂದಾಗ, ತುಂಬಾ ಹಸಿರಾಗಿದ್ದಾಗ, ಅಥವಾ ಆಮ್ಲಜನಕ ಕಡಿಮೆ ಇದ್ದಾಗ (ಬೆಳಗಿನ ಜಾವ ಮೀನುಗಳು "
                   "ಮೇಲ್ಮೈಯಲ್ಲಿ ಉಸಿರಿಗಾಗಿ ಒದ್ದಾಡಿದಾಗ) ನೀರಿನ ಒಂದು ಭಾಗವನ್ನು ಬದಲಾಯಿಸಿ, ಎಲ್ಲವನ್ನೂ ಅಲ್ಲ.",
                   "ಸ್ವಲ್ಪ ನೀರನ್ನು ಹೊರಬಿಟ್ಟು ಶುದ್ಧ ನೀರನ್ನು ತುಂಬಿಸಿ.",
                   "ಮೀನುಗಳು ಒಳಗಿರುವಾಗ ಕೊಳವನ್ನು ಖಾಲಿ ಮಾಡಬೇಡಿ."],
        },
    },
    "cleaning": {
        "words": re.compile(
            r"\b(clean|wash|scrub|desilt|sludge|silt|drain|dry\s+(out\s+)?(the|my)\s+(pond|tank|kere))\w*"
            r"|\bswachh?|\bthole"
            r"|ಸ್ವಚ್ಛ|ಶುಚಿ|ತೊಳೆ|ಕೆಸರು|ಹೂಳು|ಒಣಗಿಸ", re.I),
        "title": {"en": "Cleaning the pond or tank", "kn": "ಕೊಳ ಅಥವಾ ಟ್ಯಾಂಕ್ ಸ್ವಚ್ಛಗೊಳಿಸುವುದು"},
        "text": {
            "en": ["While fish are growing, don't fully drain or scrub the pond.",
                   "Every day, take out leftover feed and dead fish.",
                   "Between crops, after the harvest: drain the pond, remove the black sludge from the bottom, "
                   "let the bottom dry in the sun until it cracks, then fill it again."],
            "kn": ["ಮೀನುಗಳು ಬೆಳೆಯುತ್ತಿರುವಾಗ ಕೊಳವನ್ನು ಪೂರ್ತಿ ಖಾಲಿ ಮಾಡಬೇಡಿ ಅಥವಾ ಉಜ್ಜಬೇಡಿ.",
                   "ಪ್ರತಿದಿನ ಉಳಿದ ಆಹಾರ ಮತ್ತು ಸತ್ತ ಮೀನುಗಳನ್ನು ಹೊರತೆಗೆಯಿರಿ.",
                   "ಎರಡು ಬೆಳೆಗಳ ನಡುವೆ, ಕೊಯ್ಲಿನ ನಂತರ: ಕೊಳದ ನೀರನ್ನು ಖಾಲಿ ಮಾಡಿ, ತಳದ ಕಪ್ಪು ಕೆಸರನ್ನು ತೆಗೆಯಿರಿ, "
                   "ತಳ ಬಿರುಕು ಬಿಡುವವರೆಗೆ ಬಿಸಿಲಿನಲ್ಲಿ ಒಣಗಿಸಿ, ನಂತರ ಮತ್ತೆ ನೀರು ತುಂಬಿಸಿ."],
        },
        "tank": {"en": "In a tank: change part of the water and clean the bottom while the fish stay in.",
                 "kn": "ಟ್ಯಾಂಕ್‌ನಲ್ಲಿ: ಮೀನುಗಳು ಒಳಗೇ ಇರುವಾಗ ನೀರಿನ ಒಂದು ಭಾಗವನ್ನು ಬದಲಾಯಿಸಿ ಮತ್ತು ತಳವನ್ನು ಸ್ವಚ್ಛಗೊಳಿಸಿ."},
    },
    "feeding": {
        "words": re.compile(r"\bfeed\w*|\bfood\b|\baahara|ಆಹಾರ|ಮೇವು|ಉಣಿಸ|ತಿನ್ನಿಸ", re.I),
        "title": {"en": "Feeding", "kn": "ಆಹಾರ ನೀಡುವುದು"},
        "text": {
            "en": ["Feed at the same set times every day.",
                   "Give less feed on cloudy or very hot days.",
                   "Stop feeding if the fish don't eat or the oxygen is low.",
                   "If feed is left over, give less next time and take the leftover out.",
                   "For how much feed suits your fish, ask your fisheries officer or KVK."],
            "kn": ["ಪ್ರತಿದಿನ ಅದೇ ನಿಗದಿತ ಸಮಯಗಳಲ್ಲಿ ಆಹಾರ ನೀಡಿ.",
                   "ಮೋಡ ಕವಿದ ಅಥವಾ ತುಂಬಾ ಬಿಸಿಯಾದ ದಿನಗಳಲ್ಲಿ ಕಡಿಮೆ ಆಹಾರ ನೀಡಿ.",
                   "ಮೀನುಗಳು ತಿನ್ನದಿದ್ದರೆ ಅಥವಾ ಆಮ್ಲಜನಕ ಕಡಿಮೆ ಇದ್ದರೆ ಆಹಾರ ನೀಡುವುದನ್ನು ನಿಲ್ಲಿಸಿ.",
                   "ಆಹಾರ ಉಳಿದರೆ, ಮುಂದಿನ ಬಾರಿ ಕಡಿಮೆ ನೀಡಿ ಮತ್ತು ಉಳಿದದ್ದನ್ನು ಹೊರತೆಗೆಯಿರಿ.",
                   "ನಿಮ್ಮ ಮೀನುಗಳಿಗೆ ಎಷ್ಟು ಆಹಾರ ಸರಿ ಎಂದು ನಿಮ್ಮ ಮೀನುಗಾರಿಕೆ ಅಧಿಕಾರಿ ಅಥವಾ KVK ಅನ್ನು ಕೇಳಿ."],
        },
    },
    "aeration": {
        "words": re.compile(r"\baerat\w*|\bpaddle\s*wheel|ಏರೇಟರ್|ಗಾಳಿ\s*ಯಂತ್ರ", re.I),
        "title": {"en": "Aerators", "kn": "ಏರೇಟರ್"},
        "text": {
            "en": ["Run the aerator at night and before dawn, when oxygen is lowest.",
                   "It matters most after a cloudy, warm, still day.",
                   "If fish gasp at the surface, run it at once.",
                   "The Weather page shows tonight's oxygen crash risk."],
            "kn": ["ಆಮ್ಲಜನಕ ಅತಿ ಕಡಿಮೆ ಇರುವ ರಾತ್ರಿ ಮತ್ತು ಬೆಳಗಿನ ಜಾವಕ್ಕೆ ಮೊದಲು ಏರೇಟರ್ ಚಾಲನೆ ಮಾಡಿ.",
                   "ಮೋಡ ಕವಿದ, ಬಿಸಿಯಾದ, ಗಾಳಿಯಿಲ್ಲದ ದಿನದ ನಂತರ ಇದು ಅತ್ಯಂತ ಮುಖ್ಯ.",
                   "ಮೀನುಗಳು ಮೇಲ್ಮೈಯಲ್ಲಿ ಉಸಿರಿಗಾಗಿ ಒದ್ದಾಡಿದರೆ, ತಕ್ಷಣ ಚಾಲನೆ ಮಾಡಿ.",
                   "ಇಂದು ರಾತ್ರಿಯ ಆಮ್ಲಜನಕ ಕುಸಿತದ ಅಪಾಯವನ್ನು ಹವಾಮಾನ ಪುಟ ತೋರಿಸುತ್ತದೆ."],
        },
    },
    "stocking": {
        "words": re.compile(r"\bstock\w*|how many fish|overcrowd\w*|\bcrowd\w*|fingerling\w*|\bdensity"
                            r"|ಎಷ್ಟು\s*ಮೀನು|ಮೀನು\s*ಮರಿ|ಬಿತ್ತನೆ|ದಟ್ಟ", re.I),
        "title": {"en": "How many fish", "kn": "ಎಷ್ಟು ಮೀನು"},
        "text": {
            "en": ["Don't put too many fish in one pond: crowded fish get stressed, use up the oxygen and "
                   "dirty the water.",
                   "For how many fish to put in your pond, follow your hatchery or fisheries officer."],
            "kn": ["ಒಂದೇ ಕೊಳದಲ್ಲಿ ತುಂಬಾ ಮೀನುಗಳನ್ನು ಹಾಕಬೇಡಿ: ಕಿಕ್ಕಿರಿದ ಮೀನುಗಳು ಒತ್ತಡಕ್ಕೆ ಒಳಗಾಗುತ್ತವೆ, "
                   "ಆಮ್ಲಜನಕವನ್ನು ಮುಗಿಸುತ್ತವೆ ಮತ್ತು ನೀರನ್ನು ಕೊಳಕು ಮಾಡುತ್ತವೆ.",
                   "ನಿಮ್ಮ ಕೊಳಕ್ಕೆ ಎಷ್ಟು ಮೀನು ಹಾಕಬೇಕು ಎಂದು ನಿಮ್ಮ ಮರಿ ಉತ್ಪಾದನಾ ಕೇಂದ್ರ (ಹ್ಯಾಚರಿ) ಅಥವಾ "
                   "ಮೀನುಗಾರಿಕೆ ಅಧಿಕಾರಿಯ ಸಲಹೆ ಪಾಲಿಸಿ."],
        },
    },
    "checks": {
        "words": re.compile(r"\b(daily|weekly|every\s+day|every\s+week|routine)\b"
                            r"|what\s+(should|do|must)\s+i\s+(check|watch|look)"
                            r"|ಪ್ರತಿದಿನ|ದಿನನಿತ್ಯ|ವಾರಕ್ಕೊಮ್ಮೆ|ಏನು\s*ಪರಿಶೀಲಿಸ", re.I),
        "title": {"en": "Daily and weekly checks", "kn": "ದಿನನಿತ್ಯ ಮತ್ತು ವಾರದ ಪರಿಶೀಲನೆ"},
        "text": {
            "en": ["Every day at dawn, watch the fish: gasping at the surface means low oxygen.",
                   "Every day, look at the water colour and smell it: very green water or a rotten-egg smell "
                   "are warning signs.",
                   "Take out leftover feed and dead fish.",
                   "Once a week, test the water with the test kit and enter the readings in the app."],
            "kn": ["ಪ್ರತಿದಿನ ಬೆಳಗಿನ ಜಾವ ಮೀನುಗಳನ್ನು ಗಮನಿಸಿ: ಮೇಲ್ಮೈಯಲ್ಲಿ ಉಸಿರಿಗಾಗಿ ಒದ್ದಾಡುವುದು ಎಂದರೆ "
                   "ಆಮ್ಲಜನಕ ಕಡಿಮೆ.",
                   "ಪ್ರತಿದಿನ ನೀರಿನ ಬಣ್ಣ ನೋಡಿ ಮತ್ತು ವಾಸನೆ ಗಮನಿಸಿ: ತುಂಬಾ ಹಸಿರು ನೀರು ಅಥವಾ ಕೊಳೆತ ಮೊಟ್ಟೆಯ ವಾಸನೆ "
                   "ಎಚ್ಚರಿಕೆಯ ಲಕ್ಷಣಗಳು.",
                   "ಉಳಿದ ಆಹಾರ ಮತ್ತು ಸತ್ತ ಮೀನುಗಳನ್ನು ಹೊರತೆಗೆಯಿರಿ.",
                   "ವಾರಕ್ಕೊಮ್ಮೆ ಟೆಸ್ಟ್ ಕಿಟ್‌ನಿಂದ ನೀರನ್ನು ಪರೀಕ್ಷಿಸಿ ಮತ್ತು ಅಳತೆಗಳನ್ನು ಆ್ಯಪ್‌ನಲ್ಲಿ ನಮೂದಿಸಿ."],
        },
    },
}


def classify(question: str) -> str | None:
    """The pond-care topic a question is about ("cleaning", "feeding", ...), or None."""
    for topic, t in TOPICS.items():
        if t["words"].search(question):
            return topic
    return None


def answer(topic: str, question: str = "") -> dict:
    """The ready answer for a topic, in both languages. Tank questions get the tank step first."""
    t = TOPICS[topic]
    out = {}
    for lang in ("en", "kn"):
        lines = list(t["text"][lang])
        if "tank" in t:
            lines = [t["tank"][lang]] + lines if TANK_WORDS.search(question) else lines + [t["tank"][lang]]
        out[lang] = " ".join(lines + [OFFICER_NOTE[lang]])
    return out


def content_lines(lang: str) -> list[str]:
    """Pond care basics as plain text for the AI's content (docs/pond-care.md)."""
    langs = ["en", "kn"] if lang == "kn" else ["en"]
    out = ["\n## Pond care basics (docs/pond-care.md). Same care for a pond, tank or kere (ಕೆರೆ). "
           "No chemicals, liming, medicines or amounts: for those say 'ask your fisheries officer or KVK'."]
    for t in TOPICS.values():
        for lg in langs:
            extra = [t["tank"][lg]] if "tank" in t else []
            out.append(f"- {t['title'][lg]}: " + " ".join(t["text"][lg] + extra))
    for lg in langs:
        out.append(f"- {OFFICER_NOTE[lg]}")
    return out
