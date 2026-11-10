"""Conway's Game of Life on a wrapping torus, printed as text frames."""
import sys

GLIDER = {(1, 0), (2, 1), (0, 2), (1, 2), (2, 2)}


def step(cells: set, w: int, h: int) -> set:
    counts: dict = {}
    for x, y in cells:
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                if dx or dy:
                    k = ((x + dx) % w, (y + dy) % h)
                    counts[k] = counts.get(k, 0) + 1
    return {k for k, n in counts.items() if n == 3 or (n == 2 and k in cells)}


def render(cells: set, w: int, h: int) -> str:
    return "\n".join("".join("#" if (x, y) in cells else "." for x in range(w)) for y in range(h))


if __name__ == "__main__":
    gens = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    cells = set(GLIDER)
    for g in range(gens):
        print(f"gen {g}\n{render(cells, 12, 8)}\n")
        cells = step(cells, 12, 8)
