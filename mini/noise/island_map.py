"""Generate an ASCII island: fractal Perlin noise minus a radial falloff, thresholded into terrain. Usage: python island_map.py [seed]"""
import math
import sys

from perlin import Perlin

LEVELS = [(0.25, "~"), (0.32, "."), (0.55, '"'), (0.75, "^"), (9.9, "A")]


def terrain(seed: int = 7, w: int = 64, h: int = 24) -> list[str]:
    pn = Perlin(seed)
    rows = []
    for j in range(h):
        row = ""
        for i in range(w):
            nx, ny = (i / w) * 2 - 1, (j / h) * 2 - 1
            d = min(1.0, math.hypot(nx, ny))
            e = (pn.fractal(i * 0.08, j * 0.16, 5) + 0.7) / 1.4 - d * d * 0.6 + 0.2
            row += next(c for t, c in LEVELS if e < t)
        rows.append(row)
    return rows


if __name__ == "__main__":
    print("\n".join(terrain(int(sys.argv[1]) if len(sys.argv) > 1 else 7)))
