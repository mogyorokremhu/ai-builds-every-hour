"""Generate a perfect maze with randomized depth-first search and print it as ASCII."""
import random
import sys


def generate(w: int, h: int, rng: random.Random | None = None) -> list[str]:
    """Return a (2h+1) x (2w+1) grid of strings; '#' = wall, ' ' = passage."""
    rng = rng or random.Random()
    grid = [["#"] * (2 * w + 1) for _ in range(2 * h + 1)]
    stack = [(0, 0)]
    seen = {(0, 0)}
    grid[1][1] = " "
    while stack:
        x, y = stack[-1]
        nbrs = [(x + dx, y + dy) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))
                if 0 <= x + dx < w and 0 <= y + dy < h and (x + dx, y + dy) not in seen]
        if not nbrs:
            stack.pop()
            continue
        nx, ny = rng.choice(nbrs)
        grid[y + ny + 1][x + nx + 1] = " "
        grid[2 * ny + 1][2 * nx + 1] = " "
        seen.add((nx, ny))
        stack.append((nx, ny))
    return ["".join(r) for r in grid]


if __name__ == "__main__":
    w = int(sys.argv[1]) if len(sys.argv) > 1 else 15
    h = int(sys.argv[2]) if len(sys.argv) > 2 else 8
    seed = int(sys.argv[3]) if len(sys.argv) > 3 else None
    print("\n".join(generate(w, h, random.Random(seed))))
