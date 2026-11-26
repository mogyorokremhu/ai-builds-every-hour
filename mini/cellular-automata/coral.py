"""Coral (B3/S45678): a dense survive-heavy rule; small seeds mostly die back, which is the point."""
import sys

BIRTH, SURVIVE = {3}, {4, 5, 6, 7, 8}


def step(grid):
    h, w = len(grid), len(grid[0])
    out = [[0] * w for _ in range(h)]
    for y in range(h):
        for x in range(w):
            n = sum(grid[(y + dy) % h][(x + dx) % w] for dy in (-1, 0, 1) for dx in (-1, 0, 1) if dx or dy)
            out[y][x] = 1 if (n in SURVIVE if grid[y][x] else n in BIRTH) else 0
    return out


def render(grid):
    return "\n".join("".join("#" if c else "." for c in row) for row in grid)


if __name__ == "__main__":
    gens = int(sys.argv[1]) if len(sys.argv) > 1 else 24
    g = [[0] * 40 for _ in range(16)]
    for y, x in [(7, 19), (7, 20), (7, 21), (8, 19), (8, 21), (9, 20), (9, 22), (8, 23)]:
        g[y][x] = 1
    for i in range(gens + 1):
        if i in (0, gens // 2, gens):
            print(f"gen {i}")
            print(render(g))
        g = step(g)
