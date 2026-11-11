"""Rule 110 (Turing-complete) grown from a single cell on a bounded strip."""
import sys


def step(cells: list, rule: int = 110) -> list:
    n = len(cells)
    return [(rule >> (cells[(i - 1) % n] * 4 + cells[i] * 2 + cells[(i + 1) % n])) & 1 for i in range(n)]


if __name__ == "__main__":
    rows = int(sys.argv[1]) if len(sys.argv) > 1 else 24
    width = 48
    cells = [0] * width
    cells[-2] = 1
    for _ in range(rows):
        print("".join(" #"[c] for c in cells))
        cells = step(cells)
