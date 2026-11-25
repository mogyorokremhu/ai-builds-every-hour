"""Koch snowflake drawn on a character grid.

Usage: python koch_snowflake_ascii.py [depth]   (default 3, max 5)
"""
import math
import sys


def koch(p1, p2, depth):
    """Return the points of a Koch curve from p1 to p2 (excluding p2)."""
    if depth == 0:
        return [p1]
    (x1, y1), (x2, y2) = p1, p2
    dx, dy = (x2 - x1) / 3, (y2 - y1) / 3
    a = (x1 + dx, y1 + dy)
    b = (x1 + 2 * dx, y1 + 2 * dy)
    ang = -math.pi / 3
    peak = (a[0] + dx * math.cos(ang) - dy * math.sin(ang),
            a[1] + dx * math.sin(ang) + dy * math.cos(ang))
    out = []
    for s, e in ((p1, a), (a, peak), (peak, b), (b, p2)):
        out += koch(s, e, depth - 1)
    return out


def snowflake(depth):
    tri = [(0.0, 0.0), (1.0, 0.0), (0.5, math.sqrt(3) / 2)]
    # traverse so the bumps point outward
    tri = [tri[0], tri[2], tri[1], tri[0]]
    pts = []
    for i in range(3):
        pts += koch(tri[i], tri[i + 1], depth)
    pts.append(pts[0])
    return pts


def render(depth=3, width=70, height=34):
    pts = snowflake(depth)
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
    grid = [[" "] * width for _ in range(height)]
    for (ax, ay), (bx, by) in zip(pts, pts[1:]):
        for t in range(9):
            u = t / 8
            x, y = ax + (bx - ax) * u, ay + (by - ay) * u
            c = int((x - x0) / (x1 - x0) * (width - 1))
            r = int((1 - (y - y0) / (y1 - y0)) * (height - 1))
            grid[r][c] = "*"
    return "\n".join("".join(row).rstrip() for row in grid)


if __name__ == "__main__":
    d = min(5, int(sys.argv[1])) if len(sys.argv) > 1 else 3
    print(render(d))
    print(f"depth {d}: {3 * 4 ** d} segments")
