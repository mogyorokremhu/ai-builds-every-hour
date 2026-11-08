"""Rhodonea (rose) curves r = cos(k*theta). Usage: python ascii_rose.py [k ...]  (k may be a fraction like 5/3)"""
import math
import sys
from fractions import Fraction


def rose(k, size=15):
    k = Fraction(k)
    w, h = size * 4 + 1, size * 2 + 1
    grid = [[" "] * w for _ in range(h)]
    turns = k.denominator * (2 if k.numerator % 2 == 0 or k.denominator % 2 == 0 else 1)
    steps = 1500 * turns
    for s in range(steps):
        th = s / steps * math.pi * turns
        r = math.cos(float(k) * th)
        x = round(w // 2 + r * math.cos(th) * (w // 2 - 1))
        y = round(h // 2 - r * math.sin(th) * (h // 2 - 1))
        grid[y][x] = "*"
    return "\n".join("".join(r).rstrip() for r in grid)


if __name__ == "__main__":
    for k in sys.argv[1:] or ["3", "2", "5/3"]:
        print(f"k = {k}")
        print(rose(k))
