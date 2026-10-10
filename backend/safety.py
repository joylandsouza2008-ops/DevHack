"""
Safety checks shared by the Fish disease guide and the "Ask MeenuRaksha"
assistant: the app must never name chemicals, medicines or doses, and never
tell a farmer which disease their fish have.

What this file does:
    BANNED            words that must never appear in anything we show
                      (chemical and medicine names, dose words), English and Kannada.
    find_banned(text) the banned words / dose amounts found in a text.
    looks_like_diagnosis(text)  "your fish have EUS"-style sentences.
    asks_for_treatment(text)    questions asking for a medicine, chemical or dose.
    is_health_topic(text)       questions or answers about disease or treatment,
                      which must end with "confirm with your fisheries officer / KVK".
"""

from __future__ import annotations

import re

BANNED = [
    # dose words and units used for pond chemicals (mg/L is NOT here: it is our oxygen unit)
    "ppm", "kg/ha", "g/ha", "mg/kg", "g/kg", "ml/l", "dose", "dosage",
    # chemicals and medicines named in fish-disease sources
    "formalin", "formaldehyde", "malachite", "permanganate", "kmno4", "salt bath", "salt solution",
    "dipterex", "dylox", "trichlorfon", "malathion", "cypermethrin", "deltamethrin",
    "copper sulphate", "copper sulfate", "bleaching powder", "chlorine", "iodine", "povidone",
    "antibiotic", "oxytetracycline", "terramycin", "tetracycline", "erythromycin", "chloramphenicol",
    "streptomycin", "penicillin", "sulfa", "nitrofur", "ivermectin", "emamectin", "praziquantel",
    "cifax", "gammexane",
    # Kannada spellings of the most common ones
    "ಫಾರ್ಮಾಲಿನ್", "ಮಲಕೈಟ್", "ಪರ್ಮಾಂಗನೇಟ್", "ಆಂಟಿಬಯಾಟಿಕ್", "ಪ್ರತಿಜೀವಕ", "ಬ್ಲೀಚಿಂಗ್", "ಕ್ಲೋರಿನ್",
    "ಮಲಾಥಿಯಾನ್", "ಡೋಸ್", "ಮಾತ್ರೆ", "ಚುಚ್ಚುಮದ್ದು",
]

# "20 kg per acre", "5 g per litre", "2 ml/litre" ... an amount of something to add.
# A bare "/L" is not a target: "5 mg/L" is how we write oxygen and ammonia readings.
DOSE_PATTERN = re.compile(
    r"\d+(\.\d+)?\s*(kg|g|gm|gram|grams|ml|mg|litre|liter|l)\s*(/|per|a|an|each)\s*"
    r"(ha|hectare|acre|cent|litre|liter|kg|m3|tonne|pond)\b", re.IGNORECASE)

# Sentences that name a disease as THE answer, e.g. "Your fish have EUS".
DIAGNOSIS_PATTERN = re.compile(
    r"\b(your|the|these|this)\s+fish\s+(has|have|is|are)\s+(got\s+|suffering\s+from\s+|infected\s+with\s+)?"
    r"(definitely\s+|surely\s+|clearly\s+)?(eus|ich|dropsy|columnaris|argul\w*|lernae\w*|white\s+spot|"
    r"aeromon\w*|saproleg\w*|fluke\w*|gill\s+rot|anchor\s+worm|a\s+disease|an\s+infection|infected|diseased|sick\s+with)"
    r"|\b(diagnosis|diagnosed)\s+(is|as)\b"
    r"|ನಿಮ್ಮ\s+ಮೀನುಗಳಿಗೆ\s+\S+\s+(ರೋಗ\s+)?ಬಂದಿದೆ(?!\s*ಎಂದಲ್ಲ)",     # but not "... ಎಂದಲ್ಲ" (does NOT mean)
    re.IGNORECASE)

# Asking for something to put on the fish or in the pond: answered with a refusal, without the AI.
# ("How do I treat low oxygen?" is fine, so plain "treat" is not here.)
TREATMENT_WORDS = [
    "medicine", "medication", "drug", "antibiotic", "chemical", "pesticide", "dose", "dosage",
    "tablet", "injection",
    "ಔಷಧ", "ರಾಸಾಯನಿಕ", "ಡೋಸ್", "ಮಾತ್ರೆ", "ಚುಚ್ಚುಮದ್ದು", "ಎಷ್ಟು ಹಾಕ",
]
HEALTH_WORDS = TREATMENT_WORDS + [
    "cure", "treat", "ಚಿಕಿತ್ಸೆ", "ಗುಣಪಡಿಸ", "disease", "sick", "ill", "infection", "infected", "parasite", "louse", "lice", "worm", "fungus", "mould",
    "mold", "ulcer", "sore", "spot", "wound", "dying", "dead fish", "eus", "ich", "dropsy", "columnaris",
    "argul", "lernae", "fluke", "gill rot", "saproleg", "aeromon",
    "ರೋಗ", "ಸೋಂಕು", "ಹುಣ್ಣು", "ಚುಕ್ಕೆ", "ಹೇನು", "ಹುಳು", "ಬೂಷ್ಟು", "ಪರಾವಲಂಬಿ", "ಸಾಯು", "ಸತ್ತ",
]


def _contains(text: str, word: str) -> bool:
    # Latin words must match at a word start ("ich" must not match "which"); Kannada as written.
    if word.isascii() and word[0].isalpha():
        return re.search(rf"(?<![a-z]){re.escape(word)}", text) is not None
    return word in text


def find_banned(text: str) -> list[str]:
    """Banned words and dose amounts in `text` (empty list = safe)."""
    low = text.lower()
    found = [w for w in BANNED if _contains(low, w)]
    found += [m.group(0) for m in DOSE_PATTERN.finditer(text)]
    return found


def looks_like_diagnosis(text: str) -> bool:
    return DIAGNOSIS_PATTERN.search(text) is not None


def asks_for_treatment(text: str) -> bool:
    low = text.lower()
    return any(_contains(low, w) for w in TREATMENT_WORDS)


def is_health_topic(text: str) -> bool:
    low = text.lower()
    return any(_contains(low, w) for w in HEALTH_WORDS)
