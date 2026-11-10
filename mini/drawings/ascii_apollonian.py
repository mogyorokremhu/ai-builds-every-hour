"""Apollonian-style circle packing: greedy random circles that never overlap.
python ascii_apollonian.py [seed]"""
import math
import random
import sys


def main(seed: int = 3, w: int = 72, h: int = 34) -> None:
    rng = random.Random(seed)
    circles: list[tuple[float, float, float]] = []  # (x, y, r) in cell units, y stretched x2
    for _ in range(4000):
        x, y = rng.uniform(0, w), rng.uniform(0, h * 2)
        r = min(x, w - x, y, h * 2 - y)
        for cx, cy, cr in circles:
            r = min(r, math.hypot(x - cx, y - cy) - cr)
        if r > 1.2:
            circles.append((x, y, r - 0.3))
    grid = [[" "] * w for _ in range(h)]
    for j in range(h):
        for i in range(w):
            for cx, cy, cr in circles:
                d = math.hypot(i + 0.5 - cx, 2 * j + 1 - cy)
                if d <= cr:
                    grid[j][i] = "#" if d > cr - 1.2 else ("+" if cr > 4 else ".")
                    break
    print("\n".join("".join(r).rstrip() for r in grid))
    print(f"{len(circles)} circles")


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 3)
