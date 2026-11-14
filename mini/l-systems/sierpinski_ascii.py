"""Sierpinski triangle via an L-system (A/B draw, +/- turn 60 degrees), rendered as ASCII."""
import math

from expand import expand

W, H = 70, 34


def render(gens: int = 5) -> str:
    s = expand("A", {"A": "B-A-B", "B": "A+B+A"}, gens)
    # pass 1: trace path to find bounds
    pts, x, y, h = [], 0.0, 0.0, 0.0
    if gens % 2:
        h = 60.0
    for c in s:
        if c in "AB":
            x += math.cos(math.radians(h))
            y += math.sin(math.radians(h))
            pts.append((x, y))
        elif c == "+":
            h += 60
        elif c == "-":
            h -= 60
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    minx, maxx, miny, maxy = min(xs), max(xs), min(ys), max(ys)
    grid = [[" "] * W for _ in range(H)]
    for px, py in pts:
        gx = int((px - minx) / ((maxx - minx) or 1) * (W - 1))
        gy = int((py - miny) / ((maxy - miny) or 1) * (H - 1))
        grid[H - 1 - gy][gx] = "*"
    return "\n".join("".join(r).rstrip() for r in grid)


if __name__ == "__main__":
    print(render())
