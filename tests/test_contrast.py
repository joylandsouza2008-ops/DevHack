"""
Colour contrast check for the app's real colours (WCAG 2.x formula).

Reads the colour variables straight from frontend/styles.css, so changing a
colour there re-runs this check automatically. Rules:
    text                      >= 4.5 : 1
    borders, stripes, icons   >= 3   : 1

Run from the project folder with:   python -m pytest tests/test_contrast.py -v
"""

import re
from pathlib import Path

import pytest

STYLES = Path(__file__).resolve().parent.parent / "frontend" / "styles.css"


def css_colours() -> dict[str, str]:
    root = re.search(r":root\s*\{(.*?)\n\}", STYLES.read_text(encoding="utf-8"), re.S).group(1)
    return dict(re.findall(r"--([a-z-]+):\s*(#[0-9a-fA-F]{6})", root))


C = css_colours()


def luminance(hex_colour: str) -> float:
    channels = [int(hex_colour[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    linear = [c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in channels]
    return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2]


def contrast(a: str, b: str) -> float:
    hi, lo = sorted((luminance(a), luminance(b)), reverse=True)
    return (hi + 0.05) / (lo + 0.05)


TEXT, NON_TEXT = 4.5, 3.0

# (foreground, background, minimum, where it is used)
PAIRS = [
    ("text", "background", TEXT, "body text on the page"),
    ("text", "card", TEXT, "text on cards"),
    ("text-secondary", "card", TEXT, "reading names, units"),
    ("text-secondary", "surface", TEXT, "top-bar tagline"),
    ("text-secondary", "background", TEXT, "simulated clock"),
    ("text-tertiary", "card", TEXT, "tertiary text"),
    ("primary", "surface", TEXT, "app name in the top bar"),
    ("primary", "background", TEXT, "outlined button text"),
    ("on-primary", "primary", TEXT, "primary button, active toggle"),
    ("on-primary", "primary-pressed", TEXT, "pressed primary button"),
    ("on-secondary", "secondary", TEXT, "simulated-data banner, info badge"),
    ("accent", "background", TEXT, "aqua accent on the page"),
    ("accent", "card", TEXT, "aqua accent on cards"),
    ("on-accent", "accent", TEXT, "text on an aqua fill"),
    ("hairline-strong", "card", NON_TEXT, "select borders"),
    ("hairline-strong", "background", NON_TEXT, "status banner border before data"),
    ("primary", "background", NON_TEXT, "focus ring"),
    ("primary", "secondary", NON_TEXT, "dashed border of the simulated banner"),
    # Status colours (unchanged) against the new dark surfaces
    ("safe", "card", NON_TEXT, "Safe stripe on reading cards"),
    ("warning", "card", NON_TEXT, "Warning stripe on reading cards"),
    ("danger", "card", NON_TEXT, "Danger stripe on reading cards"),
    ("safe-text", "safe-bg", TEXT, "Safe banner"),
    ("warning-text", "warning-bg", TEXT, "Warning banner"),
    ("danger-text", "danger-bg", TEXT, "Danger banner, time-until-danger alert, sensor errors"),
    ("on-status", "safe", TEXT, "Safe badge"),
    ("on-warning", "warning", TEXT, "Warning badge"),
    ("on-status", "danger", TEXT, "Danger badge"),
]


@pytest.mark.parametrize("fg,bg,minimum,where", PAIRS, ids=[f"{p[0]} on {p[1]}" for p in PAIRS])
def test_contrast(fg, bg, minimum, where):
    ratio = contrast(C[fg], C[bg])
    assert ratio >= minimum, f"{where}: {fg} {C[fg]} on {bg} {C[bg]} is {ratio:.2f}:1, needs {minimum}:1"


def test_status_colours_unchanged():
    assert (C["safe"], C["warning"], C["danger"]) == ("#1a7f37", "#f5a524", "#c62828")
    assert (C["safe-bg"], C["warning-bg"], C["danger-bg"]) == ("#e6f4ea", "#fff3dc", "#fdecea")
    assert (C["safe-text"], C["warning-text"], C["danger-text"]) == ("#0d4d20", "#7a4100", "#7f1414")


def test_brand_palette_is_used():
    assert C["background"] == "#06131a" and C["text"] == "#def0f8"
    assert C["primary"] == "#88cce6" and C["secondary"] == "#1f2f91" and C["accent"] == "#22d3ee"


def test_accent_is_distinct_from_status_colours():
    # Aqua must never be mistaken for a status colour (the old red accent was, 1.5:1 from Danger).
    import math

    def oklab(h):
        rgb = [int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)]
        r, g, b = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in rgb]
        l = (0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b) ** (1 / 3)
        m = (0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b) ** (1 / 3)
        s = (0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b) ** (1 / 3)
        return (0.2104542553 * l + 0.7936177850 * m - 0.0040720468 * s,
                1.9779984951 * l - 2.4285922050 * m + 0.4505937099 * s,
                0.0259040371 * l + 0.7827717662 * m - 0.8086757660 * s)

    for status in ("safe", "warning", "danger"):
        assert 100 * math.dist(oklab(C["accent"]), oklab(C[status])) >= 15, status


def test_accent_is_never_on_buttons_or_links():
    # Aqua looks almost like primary, so it must not mark anything clickable (DESIGN.md).
    css = STYLES.read_text(encoding="utf-8") + (STYLES.parent / "welcome.css").read_text(encoding="utf-8")
    for rule in re.findall(r"([^{}]+)\{[^}]*var\(--accent\)[^}]*\}", css):
        assert not re.search(r"button|\ba\b|link|start", rule), rule


def test_danger_text_never_sits_on_the_dark_page():
    # Danger text on the dark background is unreadable; it must only appear with danger-bg.
    assert contrast(C["danger-text"], C["background"]) < TEXT     # documents why
    css = STYLES.read_text(encoding="utf-8")
    for rule in re.findall(r"\{[^}]*color:\s*var\(--danger-text\)[^}]*\}", css):
        assert "var(--danger-bg)" in rule, rule
