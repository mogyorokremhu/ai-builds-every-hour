"""Maze rule (B3/S12345): random seed grows into maze-like corridors."""
import random
import sys

BIRTH, SURVIVE = {3}, {1, 2, 3, 4, 5}


def step(grid):
    h, w = len(grid), len(grid[0])
    out = [[0] * w for _ in range(h)]
    for y in range(h):
        for x in range(w):
            n = sum(grid[(y + dy) % h][(x + dx) % w] for dy in (-1, 0, 1) for dx in (-1, 0, 1) if dx or dy)
            out[y][x] = 1 if (n in SURVIVE if grid[y][x] else n in BIRTH) else 0
    return out


def render(grid):
    return "\n".join("".join("#" if c else " " for c in row) for row in grid)


if __name__ == "__main__":
    gens = int(sys.argv[1]) if len(sys.argv) > 1 else 40
    random.seed(3)
    g = [[int(random.random() < 0.12) for _ in range(50)] for _ in range(18)]
    for _ in range(gens):
        g = step(g)
    print(render(g))
