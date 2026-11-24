"""Koch snowflake drawn with Bresenham lines on a character grid.
python ascii_koch_snowflake.py [depth]"""
import math
import sys


def koch(p1: complex, p2: complex, depth: int) -> list[complex]:
    """Return points of the Koch curve from p1 to p2 (excluding p2)."""
    if depth == 0:
        return [p1]
    d = (p2 - p1) / 3
    a, b = p1 + d, p1 + 2 * d
    peak = a + d * complex(math.cos(-math.pi / 3), math.sin(-math.pi / 3))
    pts: list[complex] = []
    for s, e in ((p1, a), (a, peak), (peak, b), (b, p2)):
        pts += koch(s, e, depth - 1)
    return pts


def line(grid: list[list[str]], x0: int, y0: int, x1: int, y1: int) -> None:
    dx, dy = abs(x1 - x0), -abs(y1 - y0)
    sx, sy = (1 if x0 < x1 else -1), (1 if y0 < y1 else -1)
    err = dx + dy
    while True:
        if 0 <= y0 < len(grid) and 0 <= x0 < len(grid[0]):
            grid[y0][x0] = "*"
        if (x0, y0) == (x1, y1):
            return
        e2 = 2 * err
        if e2 >= dy:
            err += dy
            x0 += sx
        if e2 <= dx:
            err += dx
            y0 += sy


def main(depth: int = 3, w: int = 78, h: int = 36) -> None:
    r = 16.0
    corners = [complex(r * math.cos(a), r * math.sin(a))
               for a in (math.pi / 2 + i * 2 * math.pi / 3 for i in range(3))]
    pts: list[complex] = []
    for i in range(3):
        pts += koch(corners[i], corners[(i + 1) % 3], depth)
    pts.append(pts[0])
    grid = [[" "] * w for _ in range(h)]
    cv = [(int(w / 2 + p.real * 2), int(h / 2 - p.imag + 3)) for p in pts]
    for (x0, y0), (x1, y1) in zip(cv, cv[1:]):
        line(grid, x0, y0, x1, y1)
    print("\n".join("".join(row).rstrip() for row in grid))
    print(f"depth {depth}: {len(pts) - 1} segments")


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 3)
