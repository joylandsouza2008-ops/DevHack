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


DARK_BLOCK = block(r":root")
LIGHT_BLOCK = block(r':root\[data-theme="light"\]')
THEMES = {
    "dark": hexes(DARK_BLOCK),
    "light": {**hexes(DARK_BLOCK), **hexes(LIGHT_BLOCK)},   # light inherits what it doesn't redefine (status, font)
}
ALPHAS = {"dark": rgbas(DARK_BLOCK), "light": {**rgbas(DARK_BLOCK), **rgbas(LIGHT_BLOCK)}}
C = THEMES["dark"]
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
    ("edge-on-secondary", "secondary", NON_TEXT, "dark edge on a secondary fill"),
    ("text", "footer-bg", TEXT, "active tab label in the phone tab bar, footer text"),
    ("text-secondary", "footer-bg", TEXT, "tab labels in the phone tab bar, footer links"),
    ("primary", "footer-bg", NON_TEXT, "active tab icon pill in the phone tab bar"),
    ("text", "surface", TEXT, "checklist items, test-kit inputs, SMS preview screen, status strip before data"),
    ("text-tertiary", "surface", TEXT, "time in the phone preview"),
    ("hairline-strong", "surface", NON_TEXT, "checklist item and test-kit input borders"),
    ("primary", "surface", NON_TEXT, "unticked checklist box"),
    ("primary", "card", NON_TEXT, "form message stripe, weather moon icon, live-sensor dot"),
    ("primary", "surface", NON_TEXT, "info icon on notes (simulated data, preview only)"),
    # Status colours (unchanged) against the theme's cards
    ("safe", "card", NON_TEXT, "Safe stripe on reading cards"),
    ("warning", "card", NON_TEXT, "Warning stripe on reading cards"),
    ("danger", "card", NON_TEXT, "Danger stripe on reading cards"),
    ("safe-text", "safe-bg", TEXT, "Safe banner"),
    ("warning-text", "warning-bg", TEXT, "Warning banner"),
    ("danger-text", "danger-bg", TEXT, "Danger banner, time-until-danger alert, sensor errors"),
    ("on-status", "safe", TEXT, "Safe badge"),
    ("on-warning", "warning", TEXT, "Warning badge"),
    ("on-status", "danger", TEXT, "Danger badge, Danger status strip on every page"),
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
    # Dark theme: black and white (DESIGN.md "Dark theme").
    d, l = THEMES["dark"], THEMES["light"]
    assert (d["background"], d["card"], d["hairline"], d["text"], d["text-secondary"]) == \
        ("#0a0a0a", "#141414", "#262626", "#ffffff", "#a3a3a3")
    assert (d["primary"], d["on-primary"], d["logo"]) == ("#ffffff", "#000000", "#ffffff")   # white buttons, black text
    # Light theme: the start page's palette, with one accent (teal #0B7A85).
    assert (l["background"], l["card"], l["hairline"], l["text"], l["text-secondary"]) == \
        ("#f4f7f6", "#ffffff", "#dce5e3", "#0f2a33", "#4d646b")
    assert (l["primary"], l["on-primary"], l["logo"], l["pond-fish"]) == ("#0b7a85", "#ffffff", "#0b7a85", "#0b7a85")
    # "Simulated data" tags: #E3F1F2 with teal text (a shade darker than the accent, so it reads at 4.5:1).
    assert (l["secondary"], l["on-secondary"]) == ("#e3f1f2", "#0a7680")


def test_light_theme_has_no_lavender_navy_or_bright_cyan():
    # Every light colour token is a neutral, a teal or the dark slate text (hue 170-230), apart from the status
    # colours and the unused magenta. Lavender and navy (hue 265-275) are gone.
    for name, value in THEMES["light"].items():
        if name in STATUS_TOKENS or name in ("accent", "on-accent", "warning-edge"):
            continue
        _, a, b = oklab(value)
        if math.hypot(a, b) < 0.02:
            continue                                  # a neutral grey or near-white
        hue = math.degrees(math.atan2(b, a)) % 360
        assert 170 <= hue <= 230, f"light --{name} {value} has hue {hue:.0f}"
        assert math.hypot(a, b) <= 0.1, f"light --{name} {value} is too bright (the old cyan #23bcd0 was 0.12)"


STATUS_TOKENS = {"safe", "safe-bg", "safe-text", "warning", "warning-bg", "warning-text", "on-warning",
                 "danger", "danger-bg", "danger-text", "on-status"}


def test_dark_theme_is_black_and_white():
    # No teal, blue or navy in dark mode: every colour token is a grey, except the status
    # colours (safety meaning) and the magenta accent, which nothing on screen uses.
    for name, value in THEMES["dark"].items():
        if name in STATUS_TOKENS or name in ("accent", "on-accent"):
            continue
        r, g, b = (value[i:i + 2] for i in (1, 3, 5))
        assert r == g == b, f"dark --{name} {value} is not a grey"


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


def test_pond_view_is_flat_and_follows_the_theme():
    # Light: soft teal water, deep teal fish. Dark: dark grey water, light grey fish (greys only).
    light, dark = THEMES["light"], THEMES["dark"]
    assert (light["pond-water"], light["pond-fish"]) == ("#cfe8ea", "#0b7a85")
    assert (dark["pond-water"], dark["pond-fish"]) == ("#262626", "#e5e5e5")
    for theme in (light, dark):
        assert contrast(theme["pond-fish"], theme["pond-water"]) >= NON_TEXT        # fish stand out from the water
        assert contrast(theme["pond-bubble"], theme["pond-water"]) >= 2.0           # bubbles are visible
    html = (STYLES.parent / "index.html").read_text(encoding="utf-8")
    assert 'class="pond-view" id="pond-view"' in html and "dark-scope" not in html and "dark-scope" not in CSS


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


def test_accent_is_not_used_in_the_interface():
    # Colour only means something: brand (pond blue, cyan) or Safe / Warning / Danger.
    # The magenta stays in the palette tokens, but nothing on screen uses it.
    css = CSS + (STYLES.parent / "welcome.css").read_text(encoding="utf-8")
    assert not re.findall(r"([^{}]+)\{[^}]*var\(--accent\)[^}]*\}", css)
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
        _, a, b = oklab(t[name])
        if math.hypot(a, b) < 0.02:
            continue                      # greys and near-neutral off-whites have no real hue
        for status in ("safe", "warning", "danger"):
            assert hue_gap(t[name], t[status]) >= 45, f"{theme} {name} {t[name]} is close in hue to {status}"


# ---------------------------------------------------------------- flat, calm surfaces

def test_no_decorative_background_waves():
    # The page is a plain colour: no wave artwork behind the cards.
    html = (STYLES.parent / "index.html").read_text(encoding="utf-8")
    assert "page-bg" not in html and ".page-bg" not in CSS
    assert not list((STYLES.parent / "assets").glob("background-*.svg"))


def test_one_radius_for_cards():
    # Cards, panels and banners use --radius-card; small inner parts use --radius-inner.
    assert "--radius-card: 12px;" in DARK_BLOCK and "--radius-inner: 8px;" in DARK_BLOCK
    card = re.search(r"\n\.card \{(.*?)\}", CSS, re.S).group(1)
    assert "border-radius: var(--radius-card)" in card
    for value in ("16px", "20px;", "22px", "28px", "36px"):
        rules = [r for r in re.findall(r"[^{}]+\{[^}]*border-radius:[^;]*" + value + r"[^}]*\}", CSS)
                 if not r.strip().startswith((".phone ", ".phone-screen"))]   # the drawn phone is a picture
        assert not rules, rules


def test_only_status_and_overlays_have_shadows():
    # Flat surfaces with hairline borders. The only box-shadows left are the dark amber
    # edge on Warning stripes (light theme) and the Danger strip's ring.
    for rule in re.findall(r"([^{}]+)\{[^}]*box-shadow:[^}]*\}", CSS):
        rule = re.sub(r"/\*.*?\*/", "", rule, flags=re.S).strip()
        assert "warning" in rule or "danger" in rule or "strip-breathe" in rule or rule.endswith("%"), rule
    assert "box-shadow" not in (STYLES.parent / "welcome.css").read_text(encoding="utf-8")


def test_simulated_data_chip_is_solid():
    # Calm, solid chip: cyan fill with dark text, no dashed edge (same words in both languages).
    for selector in (r"\.sim-tag \{", r"\.strip-sim \{"):
        rule = re.search(selector + r"(.*?)\}", CSS, re.S).group(1)
        assert "var(--secondary)" in rule and "var(--on-secondary)" in rule
        assert "dashed" not in rule
    assert "dashed" not in CSS


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


def test_simulated_clock_is_one_plain_line():
    # No night-scene illustration: "Simulated time: 15 Oct, 20:20, Night" and the tag, on one line.
    html = (STYLES.parent / "index.html").read_text(encoding="utf-8")
    line = html[html.index('<p class="sim-line" id="scene">'):]
    line = line[:line.index("</p>\n") + 4]
    assert 'id="sim-time"' in line and 'id="scene-phase"' in line and 'data-i18n="simulatedTag"' in line
    assert not (STYLES.parent / "scene.js").exists() and "scene-art" not in html


@both
def test_text_stays_readable_on_every_card_fill(theme):
    # Cards and the notes / inner panels (surface). Solid fills only, the same on every card.
    t = THEMES[theme]
    assert "card-deep" not in CSS
    for card in (t["card"], t["surface"]):
        assert contrast(t["text-tertiary"], card) >= TEXT, f"{theme}: {card}"
        assert contrast(t["text"], card) >= TEXT, f"{theme}: {card}"
        assert contrast(t["text-secondary"], card) >= TEXT, f"{theme}: {card}"


def test_no_glows_or_gradient_text():
    # Polish pass: no glowing blobs behind the page or cards, no gradient text,
    # no cursor spotlight. The pictures (water, sky) keep their gradients.
    css = CSS + (STYLES.parent / "welcome.css").read_text(encoding="utf-8")
    for banned in (".page-glow", ".fx-spotlight", "background-clip: text", "--card-glow", "rgba(161, 12, 159",
                   ".doodle", ".fx-ripple", ".fx-ink", ".cursor-water", "--shadow-lift"):
        assert banned not in css, banned


# ---------------------------------------------------------------- Team Orbit touches

ORBIT_CSS = CSS[CSS.index("Team Orbit touches: the credit logo"):]


LOGO = STYLES.parent / "assets" / "team-orbit-logo.svg"
FAVICON = STYLES.parent / "assets" / "team-orbit-favicon.svg"
# The Team Orbit logo, exactly as the team gave it (DESIGN.md "Team Orbit logo").
LOGO_SVG = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><mask id="to-cut" maskUnits="userSpaceOnUse">'
            '<rect width="100" height="100" fill="#fff"/><line x1="10" y1="77" x2="84" y2="27.5" stroke="#000" stroke-width="13"/>'
            '</mask></defs><circle cx="50" cy="50" r="30" fill="none" stroke="currentColor" stroke-width="11" mask="url(#to-cut)"/>'
            '<line x1="16" y1="72.5" x2="78" y2="31" stroke="currentColor" stroke-width="5" stroke-linecap="round"/>'
            '<circle cx="84" cy="27" r="8" fill="currentColor"/></svg>')
LOGO_ORBIT_LINE = '<line x1="16" y1="72.5" x2="78" y2="31" stroke="currentColor" stroke-width="5" stroke-linecap="round"/>'


def test_team_credit_on_the_welcome_screen_and_in_the_footer():
    html = (STYLES.parent / "index.html").read_text(encoding="utf-8")
    assert html.count('data-i18n="teamPresents">Team Orbit presents') == 1                     # welcome screen
    assert html.count('data-i18n="footerCredit">AquaNexus by Team Orbit (Nexus Orbit)') == 1  # footer
    assert "Built by Team Orbit" not in html and "team-credit-on-dark" not in html            # the logo replaces the pill
    # The logo inline on the start screen (top bar + flat fallback), in the header and in the footer,
    # each copy with its own mask id; the favicon is the same logo with its colours built in.
    assert html.count(LOGO_ORBIT_LINE) == 4
    masks = re.findall(r'<mask id="([^"]+)"', html)
    assert len(masks) == 4 and len(set(masks)) == 4, masks
    for mask_id in masks:
        assert html.count(f'mask="url(#{mask_id})"') == 1
    assert '<link rel="icon" href="/assets/team-orbit-favicon.svg" type="image/svg+xml">' in html


def test_team_orbit_logo_is_the_given_svg_in_the_right_colours():
    assert LOGO.read_text(encoding="utf-8").strip() == LOGO_SVG
    fav = FAVICON.read_text(encoding="utf-8")
    assert "svg{color:#0B7A85}" in fav and "(prefers-color-scheme:dark){svg{color:#FFFFFF}}" in fav
    assert LOGO_ORBIT_LINE in fav
    # Teal #0B7A85 in light mode, white in dark mode: 3:1 or better wherever the logo sits.
    assert THEMES["light"]["logo"] == "#0b7a85" and THEMES["dark"]["logo"] == "#ffffff"
    for theme in ("light", "dark"):
        for bg in ("background", "surface", "footer-bg"):
            assert contrast(THEMES[theme]["logo"], THEMES[theme][bg]) >= NON_TEXT, (theme, bg)


# The start page's own palette (welcome.css): light, and black and white in the dark theme.
WELCOME = (STYLES.parent / "welcome.css").read_text(encoding="utf-8")
_W_LIGHT = re.search(r"\n\.welcome \{(.*?)\n\}", WELCOME, re.S).group(1)
_W_DARK = re.search(r':root:not\(\[data-theme="light"\]\) \.welcome \{(.*?)\n\}', WELCOME, re.S).group(1)
W = dict(re.findall(r"--w-([a-z-]+):\s*(#[0-9a-fA-F]{6})", _W_LIGHT))
WD = dict(re.findall(r"--w-([a-z-]+):\s*(#[0-9a-fA-F]{6})", _W_DARK))


def test_start_page_is_light_and_flat():
    assert W == {"bg": "#f4f7f6", "text": "#0f2a33", "muted": "#4d646b", "accent": "#0b7a85", "line": "#dce5e3",
                 "box": "#ffffff", "on-dark": "#ffffff"}
    for banned in ("gradient(", "pond-light", "pond-caustics", ".fish", "box-shadow"):
        assert banned not in WELCOME, banned
    html = (STYLES.parent / "index.html").read_text(encoding="utf-8")
    assert '<section class="welcome" id="welcome"' in html and 'id="pond-fish"></div>' not in html


def test_start_page_text_is_readable():
    assert contrast(W["text"], W["bg"]) >= TEXT          # name, facts
    assert contrast(W["muted"], W["bg"]) >= TEXT         # tagline, fact details
    assert contrast(W["accent"], W["bg"]) >= TEXT        # "Team Orbit presents", ಮೀನು ರಕ್ಷಕ
    assert contrast(W["on-dark"], W["text"]) >= TEXT     # Start button: white on the dark text colour
    assert contrast(W["text"], W["box"]) >= TEXT         # language switch: dark on white, and white on dark
    assert contrast(W["accent"], W["bg"]) >= NON_TEXT    # logo, the orbit dot


def test_start_page_follows_the_dark_theme_in_black_and_white():
    assert WD == {"bg": "#0a0a0a", "text": "#ffffff", "muted": "#a3a3a3", "accent": "#ffffff", "line": "#262626",
                  "box": "#141414", "on-dark": "#000000"}
    assert contrast(WD["text"], WD["bg"]) >= TEXT and contrast(WD["muted"], WD["bg"]) >= TEXT
    assert contrast(WD["on-dark"], WD["text"]) >= TEXT   # white Start button with black text
    assert contrast(WD["text"], WD["box"]) >= TEXT       # language switch


def test_space_touches_use_no_status_or_accent_colour():
    # The credit logo: never a status colour or the accent.
    assert not re.search(r"var\(--(safe|warning|danger|accent)", ORBIT_CSS)


# ---------------------------------------------------------------- purposeful motion only

def test_only_purposeful_animations():
    # CSS keyframes left: the Danger banner and strip (alerts) only.
    names = set(re.findall(r"@keyframes\s+([\w-]+)", CSS + (STYLES.parent / "welcome.css").read_text(encoding="utf-8")))
    assert names == {"danger-breathe", "strip-breathe"}, names
    # No cursor effects, scroll reveals, word-by-word headings, border trails or night sky extras.
    assert not (STYLES.parent / "cursor-fx.js").exists()
    js = "".join(p.read_text(encoding="utf-8") for p in STYLES.parent.glob("*.js"))
    for banned in ("textEffect", "inView(", "borderTrail", "shootingStar", "satellitePass", "orbitTween", "fleeFrom",
                   "bindMagnet", "THREE", "Pond3D", "OrbitLogo3D", "orbit-loader"):
        assert banned not in js, banned
    # No Three.js in the project any more (the 3D pond and 3D logo are gone).
    assert not (STYLES.parent / "vendor" / "three").exists()
    assert not (STYLES.parent / "pond-3d.js").exists() and not (STYLES.parent / "orbit-logo-3d.js").exists()


def test_no_illustrations_that_are_only_decoration():
    # No drawn phone around the SMS preview, no loading animation, no badge per disease.
    html = (STYLES.parent / "index.html").read_text(encoding="utf-8")
    for gone in ('class="phone"', "phone-speaker", "orbit-loader", "weather-loader"):
        assert gone not in html, gone
    diseases = (STYLES.parent / "diseases.js").read_text(encoding="utf-8")
    assert 'make("span", "disease-cause"' in diseases and '"badge badge-info", guide.cause_types' not in diseases


def test_no_emoji_in_the_interface():
    # One outline icon set (inline SVG) everywhere; never emoji, in the page or in alert text.
    files = [*STYLES.parent.glob("*.js"), STYLES.parent / "index.html",
             *(STYLES.parent.parent / "backend").glob("*.py")]
    for path in files:
        for ch in path.read_text(encoding="utf-8"):
            assert not (0x1F000 <= ord(ch) <= 0x1FAFF or 0x2600 <= ord(ch) <= 0x27BF or ord(ch) == 0xFE0F), \
                f"{path.name}: emoji {ch!r}"


def test_welcome_screen_covers_the_sticky_dashboard():
    # The status strip and tabs (z-index 30) must never show over the welcome title.
    welcome = (STYLES.parent / "welcome.css").read_text(encoding="utf-8")
    z = int(re.search(r"\.welcome \{[^}]*z-index:\s*(\d+)", welcome, re.S).group(1))
    for other in re.findall(r"z-index:\s*(\d+)", CSS):
        if int(other) < 50:                     # 50: the ?debug panel, read-only, for developers
            assert z > int(other)
