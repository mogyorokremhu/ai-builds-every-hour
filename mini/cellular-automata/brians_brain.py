"""Brian's Brain: cells are off, firing or dying; printed as text frames."""
import random
import sys

OFF, ON, DYING = 0, 1, 2


def step(grid: list, w: int, h: int) -> list:
    new = [[OFF] * w for _ in range(h)]
    for y in range(h):
        for x in range(w):
            c = grid[y][x]
            if c == ON:
                new[y][x] = DYING
            elif c == OFF:
                n = sum(grid[(y + dy) % h][(x + dx) % w] == ON
                        for dy in (-1, 0, 1) for dx in (-1, 0, 1) if dx or dy)
                if n == 2:
                    new[y][x] = ON
    return new


def render(grid: list) -> str:
    return "\n".join("".join(".#o"[c] for c in row) for row in grid)


if __name__ == "__main__":
    gens = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    w, h = 24, 10
    rng = random.Random(7)
    grid = [[ON if rng.random() < 0.25 else OFF for _ in range(w)] for _ in range(h)]
    for g in range(gens):
        print(f"gen {g}\n{render(grid)}\n")
        grid = step(grid, w, h)
