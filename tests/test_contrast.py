"""
Colour contrast check for the app's real colours (WCAG 2.x formula).

Reads the colour variables straight from frontend/styles.css, so changing a
colour there re-runs this check automatically. Every check runs for BOTH
themes: dark (`:root, .dark-scope`) and light (`:root[data-theme="light"]`).
Rules:
    text                      >= 4.5 : 1
    borders, stripes, icons   >= 3   : 1

Run from the project folder with:   python -m pytest tests/test_contrast.py -v
"""

import math
import re
from pathlib import Path

import pytest

STYLES = Path(__file__).resolve().parent.parent / "frontend" / "styles.css"
CSS = STYLES.read_text(encoding="utf-8")
TOOL = STYLES.parent.parent / "tools" / "recolor_backgrounds.py"


def block(selector_regex: str) -> str:
    return re.search(selector_regex + r"\s*\{(.*?)\n\}", CSS, re.S).group(1)


def hexes(text: str) -> dict[str, str]:
    return dict(re.findall(r"--([a-z-]+):\s*(#[0-9a-fA-F]{6})", text))


def rgbas(text: str) -> dict[str, tuple[str, float]]:
    """--name: rgba(r, g, b, a)  ->  {name: ("#rrggbb", a)}"""
    out = {}
    for name, r, g, b, a in re.findall(r"--([a-z-]+):\s*rgba\((\d+),\s*(\d+),\s*(\d+),\s*([0-9.]+)\)", text):
        out[name] = ("#" + "".join(f"{int(v):02x}" for v in (r, g, b)), float(a))
    return out


DARK_BLOCK = block(r":root,\s*\.dark-scope")
LIGHT_BLOCK = block(r':root\[data-theme="light"\]')
THEMES = {
    "dark": hexes(DARK_BLOCK),
    "light": {**hexes(DARK_BLOCK), **hexes(LIGHT_BLOCK)},   # light inherits what it doesn't redefine (status, font)
}
ALPHAS = {"dark": rgbas(DARK_BLOCK), "light": {**rgbas(DARK_BLOCK), **rgbas(LIGHT_BLOCK)}}
C = THEMES["dark"]          # pictures (welcome, sky scene, pond view) are always dark
both = pytest.mark.parametrize("theme", ["dark", "light"])


def luminance(hex_colour: str) -> float:
    channels = [int(hex_colour[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    linear = [c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in channels]
    return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2]


def contrast(a: str, b: str) -> float:
    hi, lo = sorted((luminance(a), luminance(b)), reverse=True)
    return (hi + 0.05) / (lo + 0.05)


def over(fg: str, bg: str, alpha: float) -> str:
    """Colour seen when `fg` is drawn at `alpha` opacity over `bg`."""
    f = [int(fg[i:i + 2], 16) for i in (1, 3, 5)]
    b = [int(bg[i:i + 2], 16) for i in (1, 3, 5)]
    return "#" + "".join(f"{round(y + (x - y) * alpha):02x}" for x, y in zip(f, b))


TEXT, NON_TEXT = 4.5, 3.0

# (foreground, background, minimum, where it is used)
PAIRS = [
    ("text", "background", TEXT, "body text on the page"),
    ("text", "card", TEXT, "text on cards"),
    ("text-secondary", "card", TEXT, "reading names, units"),
    ("text-secondary", "surface", TEXT, "top-bar tagline"),
    ("text-secondary", "background", TEXT, "text directly on the page"),
    ("text-tertiary", "card", TEXT, "tertiary text"),
    ("primary", "surface", TEXT, "app name in the top bar"),
    ("primary", "background", TEXT, "outlined button text"),
    ("on-primary", "primary", TEXT, "primary button, active toggle"),
    ("on-primary", "primary-pressed", TEXT, "pressed primary button"),
    ("on-secondary", "secondary", TEXT, "simulated-data banner, info badge, selected pond (cyan fill)"),
    ("on-accent", "accent", TEXT, "text on a magenta fill (not used today; the accent is decoration only)"),
    ("hairline-strong", "card", NON_TEXT, "select borders"),
    ("hairline-strong", "background", NON_TEXT, "status banner border before data"),
    ("primary", "background", NON_TEXT, "focus ring"),
    ("edge-on-secondary", "secondary", NON_TEXT, "dashed border of the simulated banner, border trail"),
    ("text", "footer-bg", TEXT, "tonight's weather message in the bottom toolbar"),
    ("text-secondary", "footer-bg", TEXT, "tonight's weather title and details"),
    ("primary", "footer-bg", NON_TEXT, "moon icon in the bottom toolbar"),
    ("text", "surface", TEXT, "checklist items, test-kit inputs, SMS preview screen"),
    ("text-tertiary", "surface", TEXT, "time in the phone preview"),
    ("hairline-strong", "surface", NON_TEXT, "checklist item and test-kit input borders"),
    ("primary", "surface", NON_TEXT, "unticked checklist box"),
    ("primary", "card", NON_TEXT, "manual-reading tag border, form message stripe"),
    # Status colours (unchanged) against the theme's cards
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


@both
@pytest.mark.parametrize("fg,bg,minimum,where", PAIRS, ids=[f"{p[0]} on {p[1]}" for p in PAIRS])
def test_contrast(theme, fg, bg, minimum, where):
    t = THEMES[theme]
    if theme == "light" and (fg, bg) == ("warning", "card"):
        # Amber is 2:1 on a light card, so in the light theme amber stripes carry
        # a dark amber edge (--warning-edge, the unchanged warning-text): check that.
        assert contrast(t["warning"], t["card"]) < NON_TEXT     # documents why
        fg = "warning-edge"
    ratio = contrast(t[fg], t[bg])
    assert ratio >= minimum, f"{theme}: {where}: {fg} {t[fg]} on {bg} {t[bg]} is {ratio:.2f}:1, needs {minimum}:1"


def test_light_theme_amber_edge_is_the_unchanged_warning_text():
    assert THEMES["light"]["warning-edge"] == THEMES["light"]["warning-text"]
    assert "--warning-edge: transparent" in DARK_BLOCK
    assert "box-shadow: inset 2px 0 0 var(--warning-edge)" in CSS


@both
def test_status_colours_unchanged(theme):
    t = THEMES[theme]
    assert (t["safe"], t["warning"], t["danger"]) == ("#1a7f37", "#f5a524", "#c62828")
    assert (t["safe-bg"], t["warning-bg"], t["danger-bg"]) == ("#e6f4ea", "#fff3dc", "#fdecea")
    assert (t["safe-text"], t["warning-text"], t["danger-text"]) == ("#0d4d20", "#7a4100", "#7f1414")
    for name in ("safe", "warning", "danger", "safe-bg", "safe-text", "on-status"):
        assert f"--{name}:" not in LIGHT_BLOCK, "status colours are defined once, for both themes"


def test_brand_palette_is_used():
    # Dark theme: exactly the Realtime Colors palette chosen by the team.
    d, l = THEMES["dark"], THEMES["light"]
    assert (d["text"], d["background"], d["primary"], d["secondary"], d["accent"]) == \
        ("#def0f8", "#060351", "#88cce6", "#23bcd0", "#a10c9f")
    # Light theme, made from it: indigo text, deepened pond blue, same cyan and magenta.
    assert (l["text"], l["background"], l["primary"], l["secondary"], l["accent"]) == \
        ("#060351", "#eceefa", "#17698e", "#23bcd0", "#a10c9f")


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


# Colour-blindness simulation: Machado, Oliveira & Fernandes (2009), full
# severity, applied in linear RGB. Rows map (R, G, B) to what the viewer sees.
CVD = {
    "protanopia":   [[0.152286, 1.052583, -0.204868], [0.114503, 0.786281, 0.099216], [-0.003882, -0.048116, 1.051998]],
    "deuteranopia": [[0.367322, 0.860646, -0.227968], [0.280085, 0.672501, 0.047413], [-0.011820, 0.042940, 0.968881]],
    "tritanopia":   [[1.255528, -0.076749, -0.178779], [-0.078411, 0.930809, 0.147602], [0.004733, 0.691367, 0.303900]],
}


def simulate(hex_colour: str, kind: str) -> str:
    lin = lambda c: c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    enc = lambda c: 12.92 * c if c <= 0.0031308 else 1.055 * c ** (1 / 2.4) - 0.055
    rgb = [lin(int(hex_colour[i:i + 2], 16) / 255) for i in (1, 3, 5)]
    seen = [min(1, max(0, sum(row[k] * rgb[k] for k in range(3)))) for row in CVD[kind]]
    return "#" + "".join(f"{round(enc(c) * 255):02x}" for c in seen)


def colour_distance(a: str, b: str) -> float:
    return 100 * math.dist(oklab(a), oklab(b))


@both
@pytest.mark.parametrize("status", ["safe", "warning", "danger"])
def test_accent_is_distinct_from_status_colours(theme, status):
    # The magenta accent must never be mistaken for a status colour, for normal
    # vision and for red-green colour blindness (protanopia, deuteranopia).
    # 15+ = clearly different.
    a, s = THEMES[theme]["accent"], THEMES[theme][status]
    assert colour_distance(a, s) >= 15
    for kind in ("protanopia", "deuteranopia"):
        assert colour_distance(simulate(a, kind), simulate(s, kind)) >= 15, kind


def test_accent_vs_danger_for_tritanopia_is_a_known_limit():
    # Tritanopia (blue-yellow, about 1 in 10 000 people) turns this magenta into a
    # dark rose close to Danger red: distance 12, below the 15 we want (DESIGN.md
    # Known Gaps). That is acceptable only because the accent is decoration only:
    # never a fill, stripe, badge or text, never next to a status (tests below).
    # If the accent changes, this number must not get worse.
    d = colour_distance(simulate(C["accent"], "tritanopia"), simulate(C["danger"], "tritanopia"))
    assert d >= 11.5, f"{d:.1f}"


DECORATION_ONLY = {".doodle", ".sc-accent path"}     # the only places the accent may appear


def test_accent_is_decoration_only():
    # Magenta is 2.7:1 on the dark page: never text, never a control. It is used
    # only for doodles and scene lines (and, as rgba glows, in the token blocks).
    css = CSS + (STYLES.parent / "welcome.css").read_text(encoding="utf-8")
    for selector in re.findall(r"([^{}]+)\{[^}]*var\(--accent\)[^}]*\}", css):
        selector = re.sub(r"/\*.*?\*/", "", selector, flags=re.S).strip()
        assert selector in DECORATION_ONLY, selector
    for name in (STYLES.parent).glob("*.js"):
        assert "--accent" not in name.read_text(encoding="utf-8"), name.name


def test_secondary_is_a_fill_only():
    # Light theme: cyan is 2:1 on the page, so it must never be text or a border.
    assert contrast(THEMES["light"]["secondary"], THEMES["light"]["background"]) < NON_TEXT   # documents why
    for rule in re.findall(r"\{[^}]*\}", CSS):
        assert not re.search(r"(?<![-\w])(color|border[\w-]*|outline|stroke):[^;]*var\(--secondary\)", rule), rule


@both
def test_brand_colours_never_look_like_a_status_colour(theme):
    # Never green, amber or red as decoration: brand colours stay far in hue from all three.
    t = THEMES[theme]
    for name in ("background", "primary", "secondary", "accent", "surface", "card", "footer-bg"):
        for status in ("safe", "warning", "danger"):
            assert hue_gap(t[name], t[status]) >= 45, f"{theme} {name} {t[name]} is close in hue to {status}"


# ---------------------------------------------------------------- background waves

ASSETS = STYLES.parent / "assets"
WAVES = {"dark": "brand", "light": "light"}     # file suffix per theme


def wave_opacity(theme: str) -> float:
    selector = r"\.page-bg\s*\{" if theme == "dark" else r':root\[data-theme="light"\] \.page-bg\s*\{'
    rule = re.search(selector + r"(.*?)\}", CSS, re.S).group(1)
    return float(re.search(r"opacity:\s*([0-9.]+)", rule).group(1))


def wave_colours(name: str) -> list[str]:
    return re.findall(r'<path [^>]*fill="(#[0-9a-fA-F]{6})"', (ASSETS / name).read_text(encoding="utf-8"))


@both
def test_dashboard_uses_the_brand_coloured_waves(theme):
    for size in ("desktop", "phone"):
        assert f'url("/assets/background-{size}-{WAVES[theme]}.svg")' in CSS


@both
@pytest.mark.parametrize("size", ["desktop", "phone"])
def test_wave_colours_never_look_like_a_status_colour(theme, size):
    name = f"background-{size}-{WAVES[theme]}.svg"
    for colour in wave_colours(name):
        for status in ("safe", "warning", "danger"):
            assert hue_gap(colour, C[status]) >= 45, f"{name}: {colour} is close in hue to {status}"


@both
@pytest.mark.parametrize("size", ["desktop", "phone"])
def test_text_and_controls_stay_readable_over_every_wave(theme, size):
    # Dark theme: the brightest wave is the risk. Light theme: the darkest. Check them all.
    t, alpha = THEMES[theme], wave_opacity(theme)
    for colour in wave_colours(f"background-{size}-{WAVES[theme]}.svg"):
        seen = over(colour, t["background"], alpha)
        for fg, minimum in (("text", TEXT), ("text-secondary", TEXT), ("text-tertiary", TEXT),
                            ("hairline-strong", NON_TEXT), ("primary", NON_TEXT)):
            assert contrast(t[fg], seen) >= minimum, f"{theme}: {fg} over wave {colour}"


def test_wave_tool_uses_the_theme_tokens():
    tool = TOOL.read_text(encoding="utf-8")
    for suffix, theme in (("brand", "dark"), ("light", "light")):
        t = THEMES[theme]
        assert f'"{suffix}": ("{t["background"]}", "{t["primary"]}", "{t["secondary"]}")' in tool, \
            f"update THEMES in tools/recolor_backgrounds.py for the {theme} palette, then re-run it"


@pytest.mark.parametrize("name", ["background-desktop", "background-phone"])
@pytest.mark.parametrize("suffix", ["brand", "light"])
def test_brand_waves_keep_the_original_shapes(name, suffix):
    strip = lambda s: re.sub(r'fill="#[0-9a-fA-F]{6}"', "", s)
    original = (ASSETS / f"{name}.svg").read_text(encoding="utf-8")
    brand = (ASSETS / f"{name}-{suffix}.svg").read_text(encoding="utf-8")
    assert strip(original) == strip(brand), "re-run tools/recolor_backgrounds.py after editing the artwork"


# ---------------------------------------------------------------- animated dashboard

CHART_BAND_ALPHA = 0.14     # frontend/do-chart.js: status colour fill behind the line


@both
@pytest.mark.parametrize("status", ["safe", "warning", "danger"])
def test_chart_band_words_are_readable(theme, status):
    t = THEMES[theme]
    band = over(t[status], t["card"], CHART_BAND_ALPHA)
    assert contrast(t["text-secondary"], band) >= TEXT, f"band word on the {status} band"
    assert contrast(t["primary"], band) >= NON_TEXT, f"oxygen line over the {status} band"


def test_chart_band_alpha_matches_the_code():
    js = (STYLES.parent / "do-chart.js").read_text(encoding="utf-8")
    assert f"hexToRgba(z.colour, {CHART_BAND_ALPHA})" in js


@both
def test_gauge_and_pond_picker_text(theme):
    t = THEMES[theme]
    assert contrast(t["text-tertiary"], t["card"]) >= TEXT        # inactive gauge zone words
    assert contrast(t["text"], t["card"]) >= TEXT                 # active gauge word, pond names
    assert contrast(t["on-secondary"], t["secondary"]) >= TEXT    # selected pond (sliding highlight)
    assert contrast(t["edge-on-secondary"], t["secondary"]) >= NON_TEXT   # border trail on the highlight
    assert contrast(t["warning-text"], t["warning-bg"]) >= TEXT   # countdown box


def test_accent_is_never_on_buttons_or_links():
    # Aqua looks almost like primary, so it must not mark anything clickable (DESIGN.md).
    css = CSS + (STYLES.parent / "welcome.css").read_text(encoding="utf-8")
    for rule in re.findall(r"([^{}]+)\{[^}]*var\(--accent\)[^}]*\}", css):
        assert not re.search(r"button|\ba\b|link|start", rule), rule


def test_danger_text_never_sits_on_the_dark_page():
    # Danger text on the dark background is unreadable; it must only appear with danger-bg.
    assert contrast(C["danger-text"], C["background"]) < TEXT     # documents why
    for rule in re.findall(r"\{[^}]*color:\s*var\(--danger-text\)[^}]*\}", CSS):
        assert "var(--danger-bg)" in rule, rule


def test_pictures_stay_dark_in_the_light_theme():
    # Welcome pond, sky scene and pond view are night-water pictures: always dark tokens.
    html = (STYLES.parent / "index.html").read_text(encoding="utf-8")
    for element in ('class="welcome dark-scope"', 'class="scene dark-scope"', 'class="pond-view dark-scope"'):
        assert element in html
    # Text colour is inherited already computed, so the pictures must set it again from their own tokens.
    assert ".dark-scope { color: var(--text); }" in CSS


# ---------------------------------------------------------------- sky scene and cursor effects

SCENE = STYLES.parent / "scene.js"


def sky_colours() -> list[str]:
    sky = re.search(r"const SKY = \{(.*?)\};", SCENE.read_text(encoding="utf-8"), re.S).group(1)
    return re.findall(r"#[0-9a-fA-F]{6}", sky)


def test_sky_colours_never_look_like_a_status_colour():
    # Sunrise and sunset are shown with light, blue and orchid tones, never orange/red/green.
    colours = sky_colours()
    assert len(colours) == 12
    for colour in colours:
        for status in ("safe", "warning", "danger"):
            assert hue_gap(colour, C[status]) >= 45, f"sky {colour} is close in hue to {status}"


def test_scene_clock_chip_is_readable_over_the_brightest_sky():
    # The chip is rgba(4, 2, 40, 0.84) over the sky; check it over the lightest sky colour.
    assert "background: rgba(4, 2, 40, 0.84)" in CSS
    brightest = max(sky_colours(), key=luminance)
    chip = over("#040228", brightest, 0.84)
    assert contrast(C["text"], chip) >= TEXT
    assert contrast(C["text-secondary"], chip) >= TEXT
    assert contrast(C["primary"], chip) >= TEXT         # the phase word ("Night")
    assert contrast(C["on-secondary"], C["secondary"]) >= TEXT   # "Simulated data" tag


@both
def test_text_stays_readable_under_the_spotlight_and_card_gradients(theme):
    # Spotlight (--spot) under the cursor, on top of the brightest corner of each
    # card background: plain card, health card (with its glow), time-until-danger,
    # alert preview (cyan tint).
    t, a = THEMES[theme], ALPHAS[theme]
    glow, glow_alpha = a["card-glow"]
    tint, tint_alpha = a["card-secondary-tint"]
    spot, spot_alpha = a["spot"]
    for card in (t["card"], over(glow, t["card-deep-a"], glow_alpha), t["card-deep-b"], over(tint, t["card"], tint_alpha)):
        lit = over(spot, card, spot_alpha)
        assert contrast(t["text-tertiary"], lit) >= TEXT, f"{theme}: {card}"
        assert contrast(t["text"], lit) >= TEXT, f"{theme}: {card}"
        assert contrast(t["text-secondary"], lit) >= TEXT, f"{theme}: {card}"
