"""Barnsley fern via the chaos game, plotted on a character grid.

Usage: python barnsley_fern_ascii.py [points]   (default 30000)
"""
import random
import sys


def fern_points(n: int, seed: int = 1) -> list[tuple[float, float]]:
    rng = random.Random(seed)
    x = y = 0.0
    pts = []
    for _ in range(n):
        r = rng.random()
        if r < 0.01:
            x, y = 0.0, 0.16 * y
        elif r < 0.86:
            x, y = 0.85 * x + 0.04 * y, -0.04 * x + 0.85 * y + 1.6
        elif r < 0.93:
            x, y = 0.2 * x - 0.26 * y, 0.23 * x + 0.22 * y + 1.6
        else:
            x, y = -0.15 * x + 0.28 * y, 0.26 * x + 0.24 * y + 0.44
        pts.append((x, y))
    return pts


def render(n: int, width: int = 60, height: int = 30) -> str:
    grid = [[0] * width for _ in range(height)]
    for x, y in fern_points(n):
        i = int((x + 2.6) / 5.4 * (width - 1))
        j = int(y / 10.0 * (height - 1))
        if 0 <= i < width and 0 <= j < height:
            grid[j][i] += 1
    ramp = " .:*#"
    peak = max(max(r) for r in grid) or 1
    return "\n".join(
        "".join(ramp[min(4, 1 + c * 4 // peak) if c else 0] for c in row).rstrip()
        for row in reversed(grid)
    )


if __name__ == "__main__":
    print(render(int(sys.argv[1]) if len(sys.argv) > 1 else 30000))
