"""Lissajous curves plotted on a character grid.

Usage: python lissajous_ascii.py [a b phase_deg]   (default 3 2 90)
"""
import math
import sys


def plot(a: int = 3, b: int = 2, phase_deg: float = 90, w: int = 61, h: int = 25) -> str:
    grid = [[" "] * w for _ in range(h)]
    ph = math.radians(phase_deg)
    for i in range(4000):
        t = 2 * math.pi * i / 4000
        x = math.sin(a * t + ph)
        y = math.sin(b * t)
        col = round((x + 1) / 2 * (w - 1))
        row = round((1 - (y + 1) / 2) * (h - 1))
        grid[row][col] = "*"
    return "\n".join("".join(r) for r in grid)


if __name__ == "__main__":
    v = [float(x) for x in sys.argv[1:4]]
    print(plot(*(int(v[0]), int(v[1]), v[2])) if len(v) == 3 else plot())
