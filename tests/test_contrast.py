"""
Colour contrast check for the app's real colours (WCAG 2.x formula).

Reads the colour variables straight from frontend/styles.css, so changing a
colour there re-runs this check automatically. Rules:
    text                      >= 4.5 : 1
    borders, stripes, icons   >= 3   : 1

Run from the project folder with:   python -m pytest tests/test_contrast.py -v
"""

import math
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
    ("text", "footer-bg", TEXT, "tonight's weather message in the bottom toolbar"),
    ("text-secondary", "footer-bg", TEXT, "tonight's weather title and details"),
    ("primary", "footer-bg", NON_TEXT, "moon icon in the bottom toolbar"),
    ("text", "surface", TEXT, "checklist items, test-kit inputs, SMS preview screen"),
    ("text-tertiary", "surface", TEXT, "time in the phone preview"),
    ("hairline-strong", "surface", NON_TEXT, "checklist item and test-kit input borders"),
    ("primary", "surface", NON_TEXT, "unticked checklist box"),
    ("primary", "card", NON_TEXT, "manual-reading tag border, form message stripe"),
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


def oklab(h: str) -> tuple[float, float, float]:
    """Perceptual colour coordinates (OKLab). Distance x100 >= 15 = clearly different colours."""
    rgb = [int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    r, g, b = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in rgb]
    l = (0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b) ** (1 / 3)
    m = (0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b) ** (1 / 3)
    s = (0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b) ** (1 / 3)
    return (0.2104542553 * l + 0.7936177850 * m - 0.0040720468 * s,
            1.9779984951 * l - 2.4285922050 * m + 0.4505937099 * s,
            0.0259040371 * l + 0.7827717662 * m - 0.8086757660 * s)


def hue_gap(a: str, b: str) -> float:
    """Difference in hue between two colours, in degrees (0-180)."""
    ha = math.degrees(math.atan2(oklab(a)[2], oklab(a)[1])) % 360
    hb = math.degrees(math.atan2(oklab(b)[2], oklab(b)[1])) % 360
    return min(abs(ha - hb), 360 - abs(ha - hb))


def test_accent_is_distinct_from_status_colours():
    # Aqua must never be mistaken for a status colour (the old red accent was, 1.5:1 from Danger).
    for status in ("safe", "warning", "danger"):
        assert 100 * math.dist(oklab(C["accent"]), oklab(C[status])) >= 15, status


# ---------------------------------------------------------------- background waves

ASSETS = STYLES.parent / "assets"


def wave_opacity() -> float:
    rule = re.search(r"\.page-bg\s*\{(.*?)\}", STYLES.read_text(encoding="utf-8"), re.S).group(1)
    return float(re.search(r"opacity:\s*([0-9.]+)", rule).group(1))


def over(fg: str, bg: str, alpha: float) -> str:
    """Colour seen when `fg` is drawn at `alpha` opacity over `bg`."""
    f = [int(fg[i:i + 2], 16) for i in (1, 3, 5)]
    b = [int(bg[i:i + 2], 16) for i in (1, 3, 5)]
    return "#" + "".join(f"{round(y + (x - y) * alpha):02x}" for x, y in zip(f, b))


def wave_colours(name: str) -> list[str]:
    return re.findall(r'<path [^>]*fill="(#[0-9a-fA-F]{6})"', (ASSETS / name).read_text(encoding="utf-8"))


def test_dashboard_uses_the_brand_coloured_waves():
    css = STYLES.read_text(encoding="utf-8")
    assert 'url("/assets/background-desktop-brand.svg")' in css
    assert 'url("/assets/background-phone-brand.svg")' in css


@pytest.mark.parametrize("name", ["background-desktop-brand.svg", "background-phone-brand.svg"])
def test_wave_colours_never_look_like_a_status_colour(name):
    for colour in wave_colours(name):
        for status in ("safe", "warning", "danger"):
            assert hue_gap(colour, C[status]) >= 45, f"{name}: {colour} is close in hue to {status}"


@pytest.mark.parametrize("name", ["background-desktop-brand.svg", "background-phone-brand.svg"])
def test_text_and_controls_stay_readable_over_the_brightest_wave(name):
    alpha = wave_opacity()
    brightest = max((over(c, C["background"], alpha) for c in wave_colours(name)), key=luminance)
    assert contrast(C["text"], brightest) >= TEXT
    assert contrast(C["text-secondary"], brightest) >= TEXT
    assert contrast(C["text-tertiary"], brightest) >= TEXT
    assert contrast(C["hairline-strong"], brightest) >= NON_TEXT, "dropdown edges over the waves"
    assert contrast(C["primary"], brightest) >= NON_TEXT, "outlined button / focus ring over the waves"


# ---------------------------------------------------------------- animated dashboard

CHART_BAND_ALPHA = 0.14     # frontend/do-chart.js: status colour fill behind the line


@pytest.mark.parametrize("status", ["safe", "warning", "danger"])
def test_chart_band_words_are_readable(status):
    band = over(C[status], C["card"], CHART_BAND_ALPHA)
    assert contrast(C["text-secondary"], band) >= TEXT, f"band word on the {status} band"
    assert contrast(C["primary"], band) >= NON_TEXT, f"oxygen line over the {status} band"


def test_chart_band_alpha_matches_the_code():
    js = (STYLES.parent / "do-chart.js").read_text(encoding="utf-8")
    assert f"hexToRgba(z.colour, {CHART_BAND_ALPHA})" in js


def test_gauge_and_pond_picker_text():
    assert contrast(C["text-tertiary"], C["card"]) >= TEXT        # inactive gauge zone words
    assert contrast(C["text"], C["card"]) >= TEXT                 # active gauge word, pond names
    assert contrast(C["on-secondary"], C["secondary"]) >= TEXT    # selected pond (sliding highlight)
    assert contrast(C["primary"], C["secondary"]) >= NON_TEXT     # border trail on the highlight
    assert contrast(C["warning-text"], C["warning-bg"]) >= TEXT   # countdown box


@pytest.mark.parametrize("name", ["background-desktop", "background-phone"])
def test_brand_waves_keep_the_original_shapes(name):
    strip = lambda s: re.sub(r'fill="#[0-9a-fA-F]{6}"', "", s)
    original = (ASSETS / f"{name}.svg").read_text(encoding="utf-8")
    brand = (ASSETS / f"{name}-brand.svg").read_text(encoding="utf-8")
    assert strip(original) == strip(brand), "re-run tools/recolor_backgrounds.py after editing the artwork"


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


# ---------------------------------------------------------------- sky scene and cursor effects

SCENE = STYLES.parent / "scene.js"


def sky_colours() -> list[str]:
    block = re.search(r"const SKY = \{(.*?)\};", SCENE.read_text(encoding="utf-8"), re.S).group(1)
    return re.findall(r"#[0-9a-fA-F]{6}", block)


def test_sky_colours_never_look_like_a_status_colour():
    # Sunrise and sunset are shown with light and blue tones, never orange/red/green.
    colours = sky_colours()
    assert len(colours) == 12
    for colour in colours:
        for status in ("safe", "warning", "danger"):
            assert hue_gap(colour, C[status]) >= 45, f"sky {colour} is close in hue to {status}"


def test_scene_clock_chip_is_readable_over_the_brightest_sky():
    # The chip is rgba(4, 12, 18, 0.84) over the sky; check it over the lightest sky colour.
    brightest = max(sky_colours(), key=luminance)
    chip = over("#040c12", brightest, 0.84)
    assert contrast(C["text"], chip) >= TEXT
    assert contrast(C["text-secondary"], chip) >= TEXT
    assert contrast(C["primary"], chip) >= TEXT         # the phase word ("Night")
    assert contrast(C["on-secondary"], C["secondary"]) >= TEXT   # "Simulated data" tag


def test_text_stays_readable_under_the_spotlight_and_card_gradients():
    # Spotlight (aqua, alpha read from styles.css) under the cursor, on top of the
    # brightest card corners: the health card has its own 6% aqua glow too.
    css = STYLES.read_text(encoding="utf-8")
    spot = float(re.search(r"\.fx-spotlight \{[^}]*rgba\(34, 211, 238, ([0-9.]+)\)", css).group(1))
    health = over(C["accent"], "#0c2430", 0.06)
    for card in (C["card"], health, "#0b2029", over(C["secondary"], C["card"], 0.32)):
        lit = over(C["accent"], card, spot)
        assert contrast(C["text-tertiary"], lit) >= TEXT, card
        assert contrast(C["text"], lit) >= TEXT, card
