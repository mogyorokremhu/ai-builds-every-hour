"""Spirograph (hypotrochoid) curves written to an SVG file.

Usage: python spirograph_svg.py [R r d] [out.svg]   (defaults: 5 3 5 spiro.svg)
"""
import math
import sys
from math import gcd


def hypotrochoid(R: int, r: int, d: float, steps: int = 2000) -> list[tuple[float, float]]:
    """Return points of the curve traced by a point d from the centre of a circle r rolling inside R."""
    turns = r // gcd(R, r)
    pts = []
    for i in range(steps + 1):
        t = 2 * math.pi * turns * i / steps
        x = (R - r) * math.cos(t) + d * math.cos((R - r) / r * t)
        y = (R - r) * math.sin(t) - d * math.sin((R - r) / r * t)
        pts.append((x, y))
    return pts


def to_svg(pts: list[tuple[float, float]], size: int = 600) -> str:
    m = max(max(abs(x), abs(y)) for x, y in pts) or 1
    s = size / 2 * 0.95 / m
    c = size / 2
    d = " ".join(f"{'M' if i == 0 else 'L'}{c + x * s:.2f},{c + y * s:.2f}" for i, (x, y) in enumerate(pts))
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 {size} {size}">'
            f'<rect width="100%" height="100%" fill="#101020"/>'
            f'<path d="{d}" fill="none" stroke="#7fdcff" stroke-width="1"/></svg>')


def main() -> None:
    args = sys.argv[1:]
    out = "spiro.svg"
    if args and args[-1].endswith(".svg"):
        out = args.pop()
    R, r, d = (float(a) for a in args[:3]) if len(args) >= 3 else (5, 3, 5)
    svg = to_svg(hypotrochoid(int(R), int(r), d))
    with open(out, "w") as f:
        f.write(svg)
    print(f"wrote {out} ({len(svg)} bytes)")


if __name__ == "__main__":
    main()
