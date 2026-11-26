"""Generate a maze with randomized Kruskal's algorithm (union-find) — many short dead ends."""
import random
import sys


def generate(w: int, h: int, rng: random.Random | None = None) -> list[str]:
    """Return an ASCII maze grid; '#' = wall, ' ' = passage."""
    rng = rng or random.Random()
    parent = list(range(w * h))

    def find(a: int) -> int:
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    edges = [(x, y, x + 1, y) for y in range(h) for x in range(w - 1)]
    edges += [(x, y, x, y + 1) for y in range(h - 1) for x in range(w)]
    rng.shuffle(edges)
    grid = [["#"] * (2 * w + 1) for _ in range(2 * h + 1)]
    for x in range(w):
        for y in range(h):
            grid[2 * y + 1][2 * x + 1] = " "
    for x1, y1, x2, y2 in edges:
        a, b = find(y1 * w + x1), find(y2 * w + x2)
        if a != b:
            parent[a] = b
            grid[y1 + y2 + 1][x1 + x2 + 1] = " "
    return ["".join(r) for r in grid]


if __name__ == "__main__":
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else None
    print("\n".join(generate(15, 8, random.Random(seed))))
