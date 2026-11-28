"""Tiny 'Rule 110 program' runner: a 1-D cellular automaton interpreter with named rules.
Usage: python cellular_vm.py [rule] [steps]  """
import sys


def step(cells: list[int], rule: int) -> list[int]:
    n = len(cells)
    return [(rule >> (cells[(i - 1) % n] * 4 + cells[i] * 2 + cells[(i + 1) % n])) & 1
            for i in range(n)]


def run(rule: int = 110, steps: int = 16, width: int = 33) -> list[str]:
    cells = [0] * width
    cells[-2] = 1
    rows = []
    for _ in range(steps):
        rows.append("".join("#" if c else "." for c in cells))
        cells = step(cells, rule)
    return rows


if __name__ == "__main__":
    r = int(sys.argv[1]) if len(sys.argv) > 1 else 110
    s = int(sys.argv[2]) if len(sys.argv) > 2 else 16
    print("\n".join(run(r, s)))
