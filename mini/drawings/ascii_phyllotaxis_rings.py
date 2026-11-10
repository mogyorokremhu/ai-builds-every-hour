"""Concentric polygon rings with a rotating twist, ASCII.
python ascii_phyllotaxis_rings.py [sides]"""
import math
import sys


def main(sides: int = 6, w: int = 71, h: int = 35) -> None:
    grid = [[" "] * w for _ in range(h)]
    chars = "@%#*+=-:."
    for ring in range(9):
        r = 3 + ring * 1.8
        twist = ring * 0.18
        steps = 400
        for t in range(steps):
            a = 2 * math.pi * t / steps
            # polygon radius modulation
            m = math.cos(math.pi / sides) / math.cos((a + twist) % (2 * math.pi / sides) - math.pi / sides)
            x = w / 2 + r * m * math.cos(a) * 2
            y = h / 2 + r * m * math.sin(a)
            i, j = int(round(x)), int(round(y))
            if 0 <= i < w and 0 <= j < h:
                grid[j][i] = chars[ring % len(chars)]
    print("\n".join("".join(r).rstrip() for r in grid))


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 6)
