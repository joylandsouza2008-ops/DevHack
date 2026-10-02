"""
Make brand-blue copies of the dashboard background waves.

The original artwork (frontend/assets/background-desktop.svg and
background-phone.svg) uses blue, purple, pink and coral-red waves. Coral-red
behind the reading cards looks like the Danger colour, and DESIGN.md rules out
purple. This script keeps the original files unchanged and writes copies where
each wave keeps its own shape and layer, recoloured along a ramp from the brand
primary (back waves, lighter) to the brand secondary (front waves, deeper).

Run from the project folder after editing the original SVGs:
    python tools/recolor_backgrounds.py
"""

import re
from pathlib import Path

ASSETS = Path(__file__).resolve().parent.parent / "frontend" / "assets"
BACKGROUND = "#06131a"   # page background (DESIGN.md colors.background)
BACK = "#88cce6"         # colors.primary   -> the wave furthest back
FRONT = "#1f2f91"        # colors.secondary -> the wave at the front


def mix(a: str, b: str, t: float) -> str:
    """Colour t of the way from a to b (0 = a, 1 = b)."""
    ca = [int(a[i:i + 2], 16) for i in (1, 3, 5)]
    cb = [int(b[i:i + 2], 16) for i in (1, 3, 5)]
    return "#" + "".join(f"{round(x + (y - x) * t):02x}" for x, y in zip(ca, cb))


def recolor(source: Path, target: Path) -> list[str]:
    svg = source.read_text(encoding="utf-8")
    path_fill = re.compile(r'(<path [^>]*fill=")(#[0-9a-fA-F]{6})(")')
    count = len(path_fill.findall(svg))
    ramp = [mix(BACK, FRONT, i / max(1, count - 1)) for i in range(count)]
    colours = iter(ramp)   # paths are drawn back to front, in file order

    out = re.sub(r'(<rect [^>]*fill=")#[0-9a-fA-F]{6}(")', rf"\g<1>{BACKGROUND}\g<2>", svg, count=1)
    out = path_fill.sub(lambda m: m.group(1) + next(colours) + m.group(3), out)
    target.write_text(out, encoding="utf-8")
    return ramp


if __name__ == "__main__":
    for name in ("background-desktop", "background-phone"):
        ramp = recolor(ASSETS / f"{name}.svg", ASSETS / f"{name}-brand.svg")
        print(f"{name}-brand.svg: {len(ramp)} waves -> {', '.join(ramp)}")
