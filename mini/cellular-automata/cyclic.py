"""Cyclic cellular automaton: a cell advances if a neighbour holds the next state."""
import random
import sys

STATES = 5
THRESHOLD = 1


def step(grid: list) -> list:
    h, w = len(grid), len(grid[0])
    new = [row[:] for row in grid]
    for y in range(h):
        for x in range(w):
            nxt = (grid[y][x] + 1) % STATES
            n = sum(grid[(y + dy) % h][(x + dx) % w] == nxt
                    for dy in (-1, 0, 1) for dx in (-1, 0, 1) if dx or dy)
            if n >= THRESHOLD:
                new[y][x] = nxt
    return new


def render(grid: list) -> str:
    return "\n".join("".join(" .:oO"[c] for c in row) for row in grid)


if __name__ == "__main__":
    gens = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    rng = random.Random(11)
    g = [[rng.randrange(STATES) for _ in range(32)] for _ in range(10)]
    for i in range(gens + 1):
        print(f"gen {i}")
        print(render(g))
        g = step(g)
