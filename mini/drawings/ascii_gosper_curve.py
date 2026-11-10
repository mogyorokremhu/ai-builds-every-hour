"""Gosper (flowsnake) curve via an L-system, drawn on an ASCII grid.
python ascii_gosper_curve.py [order]"""
import math
import sys


def gosper(order: int) -> str:
    s = "A"
    for _ in range(order):
        s = "".join({"A": "A-B--B+A++AA+B-", "B": "+A-BB--B-A++A+B"}.get(c, c) for c in s)
    return s


def main(order: int = 3, w: int = 78, h: int = 36) -> None:
    x = y = 0.0
    ang = 0.0
    pts = [(x, y)]
    for c in gosper(order):
        if c in "AB":
            x += math.cos(ang)
            y += math.sin(ang)
            pts.append((x, y))
        elif c == "+":
            ang += math.pi / 3
        elif c == "-":
            ang -= math.pi / 3
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    sx = (w - 1) / ((max(xs) - min(xs)) or 1)
    sy = (h - 1) / ((max(ys) - min(ys)) or 1)
    k = min(sx, sy * 2)
    grid = [[" "] * w for _ in range(h)]
    for (ax, ay), (bx, by) in zip(pts, pts[1:]):
        for t in range(9):
            px = ax + (bx - ax) * t / 8
            py = ay + (by - ay) * t / 8
            i = int((px - min(xs)) * k)
            j = int((py - min(ys)) * k / 2)
            if 0 <= i < w and 0 <= j < h:
                grid[j][i] = "#"
    print("\n".join("".join(r).rstrip() for r in grid))


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 3)
