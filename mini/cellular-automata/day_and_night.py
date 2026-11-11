"""Day & Night (B3678/S34678) on a torus, printed as text frames."""
import random
import sys

BIRTH = {3, 6, 7, 8}
SURVIVE = {3, 4, 6, 7, 8}


def step(grid: list) -> list:
    h, w = len(grid), len(grid[0])
    new = [[0] * w for _ in range(h)]
    for y in range(h):
        for x in range(w):
            n = sum(grid[(y + dy) % h][(x + dx) % w]
                    for dy in (-1, 0, 1) for dx in (-1, 0, 1) if dx or dy)
            new[y][x] = int(n in (SURVIVE if grid[y][x] else BIRTH))
    return new


def render(grid: list) -> str:
    return "\n".join("".join(".#"[c] for c in row) for row in grid)


if __name__ == "__main__":
    gens = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    rng = random.Random(3)
    g = [[int(rng.random() < 0.5) for _ in range(30)] for _ in range(10)]
    for i in range(gens + 1):
        print(f"gen {i}")
        print(render(g))
        g = step(g)
