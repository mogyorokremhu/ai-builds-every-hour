"""ASCII star map with named constellations. Usage: python starmap.py [width] [height] [seed]"""
import random
import sys

SYL = ["Ka", "Ur", "Sel", "Ven", "Or", "Ta", "Ly", "Mi", "Az", "Ce"]


def build(w: int, h: int, rng: random.Random) -> list[str]:
    grid = [[" "] * w for _ in range(h)]
    for _ in range(w * h // 12):
        grid[rng.randrange(h)][rng.randrange(w)] = rng.choice(".·,'`")
    names = []
    for _ in range(3):
        x, y = rng.randrange(4, w - 4), rng.randrange(2, h - 2)
        pts = [(x, y)]
        for _ in range(rng.randint(3, 5)):
            px, py = pts[-1]
            pts.append((min(w - 1, max(0, px + rng.randint(-4, 4))), min(h - 1, max(0, py + rng.randint(-2, 2)))))
        for px, py in pts:
            grid[py][px] = "*"
        names.append((("".join(rng.choice(SYL) for _ in range(2))) + "is", pts[0]))
    for name, (px, py) in names:
        for i, c in enumerate(name):
            if px + 1 + i < w and grid[py][px + 1 + i] == " ":
                grid[py][px + 1 + i] = c
    return ["".join(r) for r in grid]


if __name__ == "__main__":
    a = sys.argv[1:]
    w = int(a[0]) if a else 60
    h = int(a[1]) if len(a) > 1 else 20
    rng = random.Random(int(a[2])) if len(a) > 2 else random.Random()
    print("\n".join(build(w, h, rng)))
