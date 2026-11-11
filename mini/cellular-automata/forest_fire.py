"""Forest fire: trees grow, lightning ignites, fire spreads to neighbouring trees."""
import random
import sys

EMPTY, TREE, FIRE = 0, 1, 2


def step(grid: list, rng: random.Random, p_grow: float = 0.03, p_light: float = 0.002) -> list:
    h, w = len(grid), len(grid[0])
    new = [[EMPTY] * w for _ in range(h)]
    for y in range(h):
        for x in range(w):
            c = grid[y][x]
            if c == FIRE:
                continue
            if c == TREE:
                burning = any(grid[(y + dy) % h][(x + dx) % w] == FIRE
                              for dx in (-1, 0, 1) for dy in (-1, 0, 1) if dx or dy)
                new[y][x] = FIRE if burning or rng.random() < p_light else TREE
            elif rng.random() < p_grow:
                new[y][x] = TREE
    return new


if __name__ == "__main__":
    gens = int(sys.argv[1]) if len(sys.argv) > 1 else 40
    rng = random.Random(3)
    grid = [[TREE if rng.random() < 0.6 else EMPTY for _ in range(40)] for _ in range(14)]
    grid[7][20] = FIRE
    for g in range(gens):
        grid = step(grid, rng)
    print(f"after {gens} generations")
    print("\n".join("".join(" ^*"[c] for c in row) for row in grid))
