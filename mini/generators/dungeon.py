"""Random-rooms dungeon map with corridors, printed as ASCII.

Usage: python dungeon.py [width] [height] [seed]
"""
import random
import sys


def generate(w: int, h: int, rng: random.Random, tries: int = 40):
    grid = [["#"] * w for _ in range(h)]
    rooms = []
    for _ in range(tries):
        rw, rh = rng.randint(4, 9), rng.randint(3, 5)
        x, y = rng.randint(1, w - rw - 2), rng.randint(1, h - rh - 2)
        if any(x < r[0] + r[2] + 1 and r[0] < x + rw + 1 and y < r[1] + r[3] + 1 and r[1] < y + rh + 1 for r in rooms):
            continue
        rooms.append((x, y, rw, rh))
        for j in range(y, y + rh):
            for i in range(x, x + rw):
                grid[j][i] = "."
    centers = [(x + rw // 2, y + rh // 2) for x, y, rw, rh in rooms]
    for (ax, ay), (bx, by) in zip(centers, centers[1:]):
        for i in range(min(ax, bx), max(ax, bx) + 1):
            grid[ay][i] = "." if grid[ay][i] == "#" else grid[ay][i]
        for j in range(min(ay, by), max(ay, by) + 1):
            grid[j][bx] = "." if grid[j][bx] == "#" else grid[j][bx]
    if centers:
        grid[centers[0][1]][centers[0][0]] = "<"
        grid[centers[-1][1]][centers[-1][0]] = ">"
    return ["".join(r) for r in grid]


if __name__ == "__main__":
    w = int(sys.argv[1]) if len(sys.argv) > 1 else 60
    h = int(sys.argv[2]) if len(sys.argv) > 2 else 20
    rng = random.Random(int(sys.argv[3])) if len(sys.argv) > 3 else random.Random()
    print("\n".join(generate(w, h, rng)))
