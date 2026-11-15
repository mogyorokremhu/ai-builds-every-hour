"""Gosper (flowsnake) curve from an L-system, drawn on a character grid."""
import math

RULES = {"A": "A-B--B+A++AA+B-", "B": "+A-BB--B-A++A+B"}


def expand(axiom: str, n: int) -> str:
    s = axiom
    for _ in range(n):
        s = "".join(RULES.get(c, c) for c in s)
    return s


def points(s: str, angle: float = 60.0):
    x = y = 0.0
    h = 0.0
    pts = [(x, y)]
    for c in s:
        if c in "AB":
            x += math.cos(math.radians(h))
            y += math.sin(math.radians(h))
            pts.append((x, y))
        elif c == "+":
            h += angle
        elif c == "-":
            h -= angle
    return pts


def render(n: int = 2, w: int = 78, h: int = 30) -> str:
    pts = points(expand("A", n))
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    sx = (w - 1) / ((max(xs) - min(xs)) or 1)
    sy = (h - 1) / ((max(ys) - min(ys)) or 1)
    grid = [[" "] * w for _ in range(h)]
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        for t in range(9):
            f = t / 8
            gx = int((x0 + (x1 - x0) * f - min(xs)) * sx)
            gy = int((y0 + (y1 - y0) * f - min(ys)) * sy)
            grid[gy][gx] = "#"
    return "\n".join("".join(r).rstrip() for r in grid)


if __name__ == "__main__":
    import sys
    print(render(int(sys.argv[1]) if len(sys.argv) > 1 else 2))
