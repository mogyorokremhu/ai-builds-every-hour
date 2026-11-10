"""Langton's ant: a tiny turmite that eventually builds a 'highway'."""
import sys


def simulate(steps: int, size: int = 21) -> list:
    grid = [[False] * size for _ in range(size)]
    x = y = size // 2
    dx, dy = 0, -1
    for _ in range(steps):
        if grid[y][x]:
            dx, dy = dy, -dx  # black: turn left
        else:
            dx, dy = -dy, dx  # white: turn right
        grid[y][x] = not grid[y][x]
        x, y = (x + dx) % size, (y + dy) % size
    return grid


if __name__ == "__main__":
    steps = int(sys.argv[1]) if len(sys.argv) > 1 else 300
    g = simulate(steps)
    print(f"Langton's ant after {steps} steps")
    print("\n".join("".join("#" if c else "." for c in r) for r in g))
