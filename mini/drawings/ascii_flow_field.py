"""Flow-field streamlines: particles follow a sine-based vector field and leave arrow-ish trails.
python ascii_flow_field.py [seed]"""
import math
import random
import sys


def main(seed: int = 5, w: int = 72, h: int = 30) -> None:
    rng = random.Random(seed)
    grid = [[" "] * w for _ in range(h)]
    glyph = "-\\|/-\\|/"
    for _ in range(60):
        x, y = rng.uniform(0, w), rng.uniform(0, h)
        for _ in range(40):
            a = math.sin(x * 0.11) + math.cos(y * 0.23) + math.sin((x + y) * 0.05)
            ang = a * math.pi
            x += math.cos(ang) * 1.5
            y += math.sin(ang) * 0.75
            if not (0 <= x < w and 0 <= y < h):
                break
            grid[int(y)][int(x)] = glyph[int((ang / (math.pi / 4)) % 8)]
    print("\n".join("".join(r).rstrip() for r in grid))


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 5)
