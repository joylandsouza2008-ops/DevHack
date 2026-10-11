"""
Where a pond is, for its weather: a fixed list of towns and villages in the
three coastal districts of Karnataka (Udupi, Dakshina Kannada, Uttara Kannada).

The farmer picks a district, then a taluk / village, from this list. There is
no GPS and no address: only the village name is stored with the pond
(backend/ponds.py). Its coordinates come from this list, and are used to
download tonight's forecast for that village (backend/weather.py).

Coordinates are the village or town centre, rounded to 2 decimals (about 1 km),
which is finer than the weather forecast grid. Every village name is unique,
so the name alone finds the place.

What this file does:
    DISTRICTS             the list: district -> taluk -> villages, in English and Kannada
    place(name)           one village by its English name, with its taluk and district (None if not in the list)
    for_page()            the list as the page's dropdowns need it (GET /api/places)
"""

from __future__ import annotations

UNKNOWN_PLACE = {"en": "Choose the village from the list.", "kn": "ಪಟ್ಟಿಯಿಂದ ಊರನ್ನು ಆರಿಸಿ."}

# (English, Kannada, latitude, longitude)
DISTRICTS = [
    {"name": {"en": "Udupi", "kn": "ಉಡುಪಿ"}, "taluks": [
        {"name": {"en": "Udupi", "kn": "ಉಡುಪಿ"}, "places": [
            ("Udupi", "ಉಡುಪಿ", 13.34, 74.74),
            ("Malpe", "ಮಲ್ಪೆ", 13.35, 74.70),
        ]},
        {"name": {"en": "Kapu", "kn": "ಕಾಪು"}, "places": [
            ("Kapu", "ಕಾಪು", 13.22, 74.75),
            ("Padubidri", "ಪಡುಬಿದ್ರಿ", 13.14, 74.77),
            ("Hejamady", "ಹೆಜಮಾಡಿ", 13.11, 74.78),
        ]},
        {"name": {"en": "Brahmavar", "kn": "ಬ್ರಹ್ಮಾವರ"}, "places": [
            ("Brahmavar", "ಬ್ರಹ್ಮಾವರ", 13.43, 74.74),
            ("Hangarakatta", "ಹಂಗಾರಕಟ್ಟೆ", 13.46, 74.72),
            ("Saligrama", "ಸಾಲಿಗ್ರಾಮ", 13.49, 74.71),
            ("Kota", "ಕೋಟ", 13.52, 74.70),
        ]},
        {"name": {"en": "Kundapura", "kn": "ಕುಂದಾಪುರ"}, "places": [
            ("Kundapura", "ಕುಂದಾಪುರ", 13.62, 74.69),
            ("Koteshwara", "ಕೋಟೇಶ್ವರ", 13.60, 74.70),
            ("Gangolli", "ಗಂಗೊಳ್ಳಿ", 13.65, 74.67),
        ]},
        {"name": {"en": "Byndoor", "kn": "ಬೈಂದೂರು"}, "places": [
            ("Maravanthe", "ಮರವಂತೆ", 13.70, 74.64),
            ("Byndoor", "ಬೈಂದೂರು", 13.87, 74.63),
            ("Shiroor", "ಶಿರೂರು", 13.92, 74.60),
        ]},
        {"name": {"en": "Karkala", "kn": "ಕಾರ್ಕಳ"}, "places": [
            ("Karkala", "ಕಾರ್ಕಳ", 13.21, 74.99),
        ]},
        {"name": {"en": "Hebri", "kn": "ಹೆಬ್ರಿ"}, "places": [
            ("Hebri", "ಹೆಬ್ರಿ", 13.46, 74.99),
        ]},
    ]},
    {"name": {"en": "Dakshina Kannada", "kn": "ದಕ್ಷಿಣ ಕನ್ನಡ"}, "taluks": [
        {"name": {"en": "Mangaluru", "kn": "ಮಂಗಳೂರು"}, "places": [
            ("Mangaluru", "ಮಂಗಳೂರು", 12.9141, 74.8560),     # same point as the demo pond's weather
            ("Bengre", "ಬೆಂಗ್ರೆ", 12.87, 74.83),
            ("Surathkal", "ಸುರತ್ಕಲ್", 13.00, 74.79),
        ]},
        {"name": {"en": "Mulki", "kn": "ಮೂಲ್ಕಿ"}, "places": [
            ("Mulki", "ಮೂಲ್ಕಿ", 13.09, 74.79),
            ("Sasihithlu", "ಸಸಿಹಿತ್ಲು", 13.07, 74.78),
        ]},
        {"name": {"en": "Ullal", "kn": "ಉಳ್ಳಾಲ"}, "places": [
            ("Ullal", "ಉಳ್ಳಾಲ", 12.80, 74.85),
            ("Someshwara", "ಸೋಮೇಶ್ವರ", 12.79, 74.85),
        ]},
        {"name": {"en": "Moodbidri", "kn": "ಮೂಡುಬಿದಿರೆ"}, "places": [
            ("Moodbidri", "ಮೂಡುಬಿದಿರೆ", 13.07, 75.00),
        ]},
        {"name": {"en": "Bantwal", "kn": "ಬಂಟ್ವಾಳ"}, "places": [
            ("Bantwal", "ಬಂಟ್ವಾಳ", 12.89, 75.03),
        ]},
        {"name": {"en": "Puttur", "kn": "ಪುತ್ತೂರು"}, "places": [
            ("Puttur", "ಪುತ್ತೂರು", 12.76, 75.20),
        ]},
        {"name": {"en": "Belthangady", "kn": "ಬೆಳ್ತಂಗಡಿ"}, "places": [
            ("Belthangady", "ಬೆಳ್ತಂಗಡಿ", 12.98, 75.30),
        ]},
        {"name": {"en": "Sullia", "kn": "ಸುಳ್ಯ"}, "places": [
            ("Sullia", "ಸುಳ್ಯ", 12.56, 75.39),
        ]},
    ]},
    {"name": {"en": "Uttara Kannada", "kn": "ಉತ್ತರ ಕನ್ನಡ"}, "taluks": [
        {"name": {"en": "Karwar", "kn": "ಕಾರವಾರ"}, "places": [
            ("Karwar", "ಕಾರವಾರ", 14.81, 74.13),
            ("Majali", "ಮಾಜಾಳಿ", 14.90, 74.10),
        ]},
        {"name": {"en": "Ankola", "kn": "ಅಂಕೋಲಾ"}, "places": [
            ("Ankola", "ಅಂಕೋಲಾ", 14.66, 74.30),
        ]},
        {"name": {"en": "Kumta", "kn": "ಕುಮಟಾ"}, "places": [
            ("Gokarna", "ಗೋಕರ್ಣ", 14.55, 74.32),
            ("Kumta", "ಕುಮಟಾ", 14.43, 74.42),
        ]},
        {"name": {"en": "Honnavar", "kn": "ಹೊನ್ನಾವರ"}, "places": [
            ("Honnavar", "ಹೊನ್ನಾವರ", 14.28, 74.44),
        ]},
        {"name": {"en": "Bhatkal", "kn": "ಭಟ್ಕಳ"}, "places": [
            ("Murdeshwar", "ಮುರ್ಡೇಶ್ವರ", 14.09, 74.48),
            ("Bhatkal", "ಭಟ್ಕಳ", 13.99, 74.56),
        ]},
        {"name": {"en": "Sirsi", "kn": "ಶಿರಸಿ"}, "places": [
            ("Sirsi", "ಶಿರಸಿ", 14.62, 74.84),
        ]},
        {"name": {"en": "Yellapur", "kn": "ಯಲ್ಲಾಪುರ"}, "places": [
            ("Yellapur", "ಯಲ್ಲಾಪುರ", 14.96, 74.71),
        ]},
    ]},
]


def _index() -> dict[str, dict]:
    found = {}
    for district in DISTRICTS:
        for taluk in district["taluks"]:
            for en, kn, latitude, longitude in taluk["places"]:
                found[en] = {"village": en, "name": {"en": en, "kn": kn}, "taluk": taluk["name"],
                             "district": district["name"], "latitude": latitude, "longitude": longitude}
    return found


BY_NAME = _index()


def place(name: str | None) -> dict | None:
    """'Kota' -> {village, name, taluk, district, latitude, longitude}. None if it isn't in the list."""
    return BY_NAME.get(" ".join((name or "").split()))


def for_page() -> dict:
    """The districts, taluks and villages for the page's two dropdowns (no coordinates needed there)."""
    return {"districts": [
        {"name": d["name"], "taluks": [
            {"name": t["name"], "places": [{"village": en, "name": {"en": en, "kn": kn}} for en, kn, _, _ in t["places"]]}
            for t in d["taluks"]]}
        for d in DISTRICTS]}
