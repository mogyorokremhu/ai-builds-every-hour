"""Render an L-system as an SVG file using a tiny turtle (no dependencies)."""
import math
import sys

from expand import SYSTEMS, expand


def draw(s: str, angle: float, step: float = 5.0) -> list[tuple[float, float, float, float]]:
    """Interpret F/G as forward, +/- as turns, [ ] as push/pop; return segments."""
    x = y = 0.0
    heading = -90.0
    stack, segs = [], []
    for c in s:
        if c in "FG":
            nx = x + step * math.cos(math.radians(heading))
            ny = y + step * math.sin(math.radians(heading))
            segs.append((x, y, nx, ny))
            x, y = nx, ny
        elif c == "+":
            heading += angle
        elif c == "-":
            heading -= angle
        elif c == "[":
            stack.append((x, y, heading))
        elif c == "]":
            x, y, heading = stack.pop()
    return segs


def to_svg(segs) -> str:
    xs = [v for s in segs for v in (s[0], s[2])]
    ys = [v for s in segs for v in (s[1], s[3])]
    x0, y0 = min(xs) - 5, min(ys) - 5
    w, h = max(xs) - x0 + 5, max(ys) - y0 + 5
    lines = "".join(
        f'<line x1="{a-x0:.1f}" y1="{b-y0:.1f}" x2="{c-x0:.1f}" y2="{d-y0:.1f}"/>'
        for a, b, c, d in segs
    )
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w:.0f}" height="{h:.0f}">'
            f'<rect width="100%" height="100%" fill="#111"/>'
            f'<g stroke="#7fdc7f" stroke-width="1">{lines}</g></svg>')


ANGLES = {"koch": 90, "dragon": 90, "plant": 25, "algae": 90}

if __name__ == "__main__":
    name = sys.argv[1] if len(sys.argv) > 1 else "plant"
    gens = int(sys.argv[2]) if len(sys.argv) > 2 else 4
    axiom, rules = SYSTEMS[name]
    svg = to_svg(draw(expand(axiom, rules, gens), ANGLES[name]))
    out = f"{name}.svg"
    with open(out, "w") as f:
        f.write(svg)
    print(f"wrote {out} ({len(svg)} bytes)")
