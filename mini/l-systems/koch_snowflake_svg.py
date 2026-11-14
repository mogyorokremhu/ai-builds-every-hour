"""Koch snowflake from an L-system, written as an SVG file.

Usage: python koch_snowflake_svg.py [iterations] [out.svg]
"""
import math
import sys


def expand(axiom: str, rules: dict, n: int) -> str:
    for _ in range(n):
        axiom = "".join(rules.get(c, c) for c in axiom)
    return axiom


def points(s: str, step: float = 4.0, angle: float = 60.0):
    x = y = 0.0
    h = 0.0
    pts = [(x, y)]
    for c in s:
        if c == "F":
            x += step * math.cos(math.radians(h))
            y += step * math.sin(math.radians(h))
            pts.append((x, y))
        elif c == "+":
            h += angle
        elif c == "-":
            h -= angle
    return pts


def main() -> None:
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    out = sys.argv[2] if len(sys.argv) > 2 else "koch.svg"
    s = expand("F--F--F", {"F": "F+F--F+F"}, n)
    pts = points(s, step=max(0.5, 4.0 / 3 ** (n - 1)) * 3)
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    x0, y0 = min(xs) - 10, min(ys) - 10
    w, h = max(xs) - x0 + 10, max(ys) - y0 + 10
    path = " ".join(f"{x - x0:.2f},{y - y0:.2f}" for x, y in pts)
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w:.0f}" height="{h:.0f}">'
           f'<rect width="100%" height="100%" fill="#0b1020"/>'
           f'<polygon points="{path}" fill="#bde0fe" stroke="#fff" stroke-width="0.5"/></svg>')
    with open(out, "w") as f:
        f.write(svg)
    print(f"wrote {out} ({len(pts)} points)")


if __name__ == "__main__":
    main()
