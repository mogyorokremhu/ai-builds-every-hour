"""Heighway dragon curve drawn on a character grid.

Usage: python dragon_curve_ascii.py [order]   (default 9)
"""
import sys


def dragon_turns(order: int) -> list[int]:
    """Turn sequence (+1 left, -1 right) of the dragon curve of the given order."""
    turns: list[int] = []
    for _ in range(order):
        turns = turns + [1] + [-t for t in reversed(turns)]
    return turns


def dragon_points(order: int) -> list[tuple[int, int]]:
    x = y = 0
    dx, dy = 1, 0
    pts = [(x, y)]
    x, y = x + dx, y + dy
    pts.append((x, y))
    for t in dragon_turns(order):
        dx, dy = (-dy, dx) if t == 1 else (dy, -dx)
        x, y = x + dx, y + dy
        pts.append((x, y))
    return pts


def render(order: int) -> str:
    pts = dragon_points(order)
    x0 = min(p[0] for p in pts)
    y0 = min(p[1] for p in pts)
    w = (max(p[0] for p in pts) - x0) * 2 + 1
    h = (max(p[1] for p in pts) - y0) * 2 + 1
    grid = [[" "] * w for _ in range(h)]
    for (ax, ay), (bx, by) in zip(pts, pts[1:]):
        gx, gy = (ax - x0) * 2, (ay - y0) * 2
        hx, hy = (bx - x0) * 2, (by - y0) * 2
        grid[gy][gx] = grid[hy][hx] = "+"
        mx, my = (gx + hx) // 2, (gy + hy) // 2
        grid[my][mx] = "-" if ay == by else "|"
    return "\n".join("".join(r).rstrip() for r in reversed(grid))


if __name__ == "__main__":
    print(render(int(sys.argv[1]) if len(sys.argv) > 1 else 9))
