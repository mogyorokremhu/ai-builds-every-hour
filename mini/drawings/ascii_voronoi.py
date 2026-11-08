"""Voronoi diagram in ASCII: random seed points, each cell filled with its own letter and
borders drawn where neighbouring cells meet.

    python ascii_voronoi.py            # 14 cells, random layout
    python ascii_voronoi.py 25 7       # 25 cells, seed 7
    python ascii_voronoi.py 12 3 --manhattan
"""
import random
import sys

W, H = 78, 28
ASPECT = 0.5  # terminal cells are about twice as tall as they are wide


def nearest(x: float, y: float, sites: list[tuple[float, float]], manhattan: bool) -> int:
    """Index of the site closest to (x, y)."""
    best, best_d = 0, float("inf")
    for i, (sx, sy) in enumerate(sites):
        dx, dy = x - sx, (y - sy) / ASPECT
        d = abs(dx) + abs(dy) if manhattan else dx * dx + dy * dy
        if d < best_d:
            best, best_d = i, d
    return best


def voronoi(n: int, seed: int, manhattan: bool = False, w: int = W, h: int = H) -> list[str]:
    """Render the diagram as a list of text rows."""
    rng = random.Random(seed)
    sites = [(rng.uniform(0, w - 1), rng.uniform(0, h - 1)) for _ in range(n)]
    owner = [[nearest(x, y, sites, manhattan) for x in range(w)] for y in range(h)]
    letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    rows = []
    for y in range(h):
        line = []
        for x in range(w):
            me = owner[y][x]
            right = owner[y][x + 1] if x + 1 < w else me
            down = owner[y + 1][x] if y + 1 < h else me
            if right != me and down != me:
                ch = "+"
            elif right != me:
                ch = "|"
            elif down != me:
                ch = "-"
            else:
                ch = letters[me % len(letters)] if (x + y) % 3 == 0 else " "
            line.append(ch)
        rows.append(line)
    for i, (sx, sy) in enumerate(sites):
        rows[round(sy)][round(sx)] = "@"
    return ["".join(r) for r in rows]


def main(argv: list[str]) -> None:
    """Parse arguments and print the diagram."""
    args = [a for a in argv if not a.startswith("--")]
    n = int(args[0]) if args else 14
    seed = int(args[1]) if len(args) > 1 else random.randrange(10**6)
    manhattan = "--manhattan" in argv
    print("\n".join(voronoi(n, seed, manhattan)))
    print(f"{n} cells, seed {seed}, {'Manhattan' if manhattan else 'Euclidean'} distance (@ = site)")


if __name__ == "__main__":
    main(sys.argv[1:])
