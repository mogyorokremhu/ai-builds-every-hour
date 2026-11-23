"""Hilbert space-filling curve drawn with box characters.

Usage: python hilbert_curve_ascii.py [order]   (default 3)
"""
import sys


def d2xy(order: int, d: int) -> tuple[int, int]:
    """Map index d along the Hilbert curve to (x, y) on a 2**order grid."""
    x = y = 0
    t = d
    s = 1
    while s < (1 << order):
        rx = 1 & (t // 2)
        ry = 1 & (t ^ rx)
        if ry == 0:
            if rx == 1:
                x, y = s - 1 - x, s - 1 - y
            x, y = y, x
        x += s * rx
        y += s * ry
        t //= 4
        s *= 2
    return x, y


def render(order: int) -> str:
    n = 1 << order
    w, h = n * 2 - 1, n * 2 - 1
    grid = [[" "] * w for _ in range(h)]
    pts = [d2xy(order, d) for d in range(n * n)]
    for x, y in pts:
        grid[y * 2][x * 2] = "o"
    for (ax, ay), (bx, by) in zip(pts, pts[1:]):
        if ay == by:
            grid[ay * 2][ax + bx] = "-"
        else:
            grid[ay + by][ax * 2] = "|"
    return "\n".join("".join(r) for r in grid)


if __name__ == "__main__":
    print(render(int(sys.argv[1]) if len(sys.argv) > 1 else 3))
