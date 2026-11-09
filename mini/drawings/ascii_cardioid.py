"""Cardioid envelope: chords joining point k to point 2k on a circle (string art)."""
import math
import sys


def draw(points: int = 60, w: int = 61, h: int = 31) -> str:
    g = [[" "] * w for _ in range(h)]
    pos = [(w // 2 + (w // 2 - 1) * math.cos(2 * math.pi * i / points),
            h // 2 + (h // 2 - 1) * math.sin(2 * math.pi * i / points)) for i in range(points)]
    for i in range(points):
        (x0, y0), (x1, y1) = pos[i], pos[(2 * i) % points]
        for s in range(41):
            t = s / 40
            x, y = round(x0 + (x1 - x0) * t), round(y0 + (y1 - y0) * t)
            g[y][x] = "*" if g[y][x] != " " else "."
    return "\n".join("".join(r).rstrip() for r in g)


if __name__ == "__main__":
    print(draw(int(sys.argv[1]) if len(sys.argv) > 1 else 60))
