"""HighLife (B36/S23) seeded with the R-pentomino, printed as text frames."""
import sys

REPLICATOR = {(x + 8, y + 6) for x, y in {(1, 0), (2, 0), (0, 1), (1, 1), (1, 2)}}


def step(cells: set) -> set:
    counts: dict = {}
    for x, y in cells:
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                if dx or dy:
                    counts[(x + dx, y + dy)] = counts.get((x + dx, y + dy), 0) + 1
    return {k for k, n in counts.items()
            if (k in cells and n in (2, 3)) or (k not in cells and n in (3, 6))}


def render(cells: set, w: int = 24, h: int = 16) -> str:
    return "\n".join("".join("#" if (x, y) in cells else "." for x in range(w)) for y in range(h))


if __name__ == "__main__":
    gens = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    cells = set(REPLICATOR)
    for g in range(gens):
        print(f"gen {g} ({len(cells)} cells)\n{render(cells)}\n")
        cells = step(cells)
