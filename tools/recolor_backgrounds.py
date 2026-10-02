"""
Make brand-coloured copies of the dashboard background waves, one per theme.

The original artwork (frontend/assets/background-desktop.svg and
background-phone.svg) uses blue, purple, pink and coral-red waves. Pink and
coral-red behind the reading cards look like the Danger colour. This script
keeps the original files unchanged and writes copies where
each wave keeps its own shape and layer, recoloured along a ramp from the brand
primary (back waves) to the brand secondary (front waves):

    *-brand.svg   dark theme  (page background + dark-theme primary/secondary)
    *-light.svg   light theme (page background + light-theme primary/secondary)

The colours below must match the theme tokens in frontend/styles.css
(tests/test_contrast.py checks that they do).

Run from the project folder after editing the original SVGs or the palette:
    python tools/recolor_backgrounds.py
"""

import re
from pathlib import Path

ASSETS = Path(__file__).resolve().parent.parent / "frontend" / "assets"

# suffix: (page background, back wave = primary, front wave = secondary)
THEMES = {
    "brand": ("#060351", "#88cce6", "#23bcd0"),   # dark theme
    "light": ("#eceefa", "#17698e", "#23bcd0"),   # light theme
}


def mix(a: str, b: str, t: float) -> str:
    """Colour t of the way from a to b (0 = a, 1 = b)."""
    ca = [int(a[i:i + 2], 16) for i in (1, 3, 5)]
    cb = [int(b[i:i + 2], 16) for i in (1, 3, 5)]
    return "#" + "".join(f"{round(x + (y - x) * t):02x}" for x, y in zip(ca, cb))


def recolor(source: Path, target: Path, background: str, back: str, front: str) -> list[str]:
    svg = source.read_text(encoding="utf-8")
    path_fill = re.compile(r'(<path [^>]*fill=")(#[0-9a-fA-F]{6})(")')
    count = len(path_fill.findall(svg))
    ramp = [mix(back, front, i / max(1, count - 1)) for i in range(count)]
    colours = iter(ramp)   # paths are drawn back to front, in file order

    out = re.sub(r'(<rect [^>]*fill=")#[0-9a-fA-F]{6}(")', rf"\g<1>{background}\g<2>", svg, count=1)
    out = path_fill.sub(lambda m: m.group(1) + next(colours) + m.group(3), out)
    target.write_text(out, encoding="utf-8")
    return ramp


if __name__ == "__main__":
    for name in ("background-desktop", "background-phone"):
        for suffix, (background, back, front) in THEMES.items():
            ramp = recolor(ASSETS / f"{name}.svg", ASSETS / f"{name}-{suffix}.svg", background, back, front)
            print(f"{name}-{suffix}.svg: {len(ramp)} waves -> {', '.join(ramp)}")
