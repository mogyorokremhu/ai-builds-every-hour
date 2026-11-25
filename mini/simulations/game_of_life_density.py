"""Conway's Life on a torus: how final live-cell density depends on initial density. Usage: python game_of_life_density.py [size] [steps]"""
import random
import sys


def step(grid):
    n = len(grid)
    new = [[0] * n for _ in range(n)]
    for y in range(n):
        for x in range(n):
            s = sum(grid[(y + dy) % n][(x + dx) % n] for dy in (-1, 0, 1) for dx in (-1, 0, 1)) - grid[y][x]
            new[y][x] = 1 if s == 3 or (s == 2 and grid[y][x]) else 0
    return new


def run(size: int, steps: int, p: float, seed: int = 1) -> float:
    rng = random.Random(seed)
    g = [[1 if rng.random() < p else 0 for _ in range(size)] for _ in range(size)]
    for _ in range(steps):
        g = step(g)
    return sum(map(sum, g)) / (size * size)


if __name__ == "__main__":
    size = int(sys.argv[1]) if len(sys.argv) > 1 else 32
    steps = int(sys.argv[2]) if len(sys.argv) > 2 else 100
    for p in (0.1, 0.2, 0.3, 0.4, 0.5, 0.7):
        d = run(size, steps, p)
        print(f"initial {p:.1f} -> final {d:.3f} {'#' * int(d * 100)}")
