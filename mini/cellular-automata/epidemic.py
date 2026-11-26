"""SIR-style epidemic CA: susceptible, infected (timed), recovered on a torus."""
import random
import sys

S, I, R = 0, 1, 2
INFECT_P, DURATION = 0.35, 4


def step(grid, timers, rng):
    h, w = len(grid), len(grid[0])
    g2 = [row[:] for row in grid]
    t2 = [row[:] for row in timers]
    for y in range(h):
        for x in range(w):
            if grid[y][x] == S:
                n = sum(grid[(y + dy) % h][(x + dx) % w] == I for dy, dx in ((-1, 0), (1, 0), (0, -1), (0, 1)))
                if n and rng.random() < 1 - (1 - INFECT_P) ** n:
                    g2[y][x], t2[y][x] = I, DURATION
            elif grid[y][x] == I:
                t2[y][x] -= 1
                if t2[y][x] <= 0:
                    g2[y][x] = R
    return g2, t2


def render(grid):
    return "\n".join("".join(".#o"[c] for c in row) for row in grid)


if __name__ == "__main__":
    gens = int(sys.argv[1]) if len(sys.argv) > 1 else 30
    rng = random.Random(3)
    h, w = 14, 40
    grid = [[S] * w for _ in range(h)]
    timers = [[0] * w for _ in range(h)]
    grid[h // 2][w // 2], timers[h // 2][w // 2] = I, DURATION
    for i in range(gens + 1):
        if i % 10 == 0:
            flat = [c for r in grid for c in r]
            print(f"gen {i}: S={flat.count(S)} I={flat.count(I)} R={flat.count(R)}")
            print(render(grid))
        grid, timers = step(grid, timers, rng)
