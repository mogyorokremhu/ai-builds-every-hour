"""ASCII city skyline generator. Usage: python city_skyline.py [width] [height] [seed]"""
import random
import sys


def skyline(width: int, height: int, rng: random.Random) -> str:
    grid = [[" "] * width for _ in range(height)]
    x = 0
    while x < width:
        w = min(rng.randint(3, 7), width - x)
        h = rng.randint(2, height - 1)
        for dx in range(w):
            for dy in range(h):
                row = height - 1 - dy
                edge = dx in (0, w - 1)
                top = dy == h - 1
                if top or edge:
                    grid[row][x + dx] = "_" if top and not edge else "|"
                elif dx % 2 == 1 and dy % 2 == 1:
                    grid[row][x + dx] = rng.choice("o.o#")
        x += w + rng.randint(0, 1)
    return "\n".join("".join(r).rstrip() for r in grid) + "\n" + "=" * width


if __name__ == "__main__":
    a = sys.argv[1:]
    rng = random.Random(int(a[2])) if len(a) > 2 else random.Random()
    print(skyline(int(a[0]) if a else 50, int(a[1]) if len(a) > 1 else 10, rng))
