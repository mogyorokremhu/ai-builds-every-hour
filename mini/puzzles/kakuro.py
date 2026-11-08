#!/usr/bin/env python3
"""Kakuro (cross sums) solver.

White cells take digits 1-9; every horizontal and vertical run of white cells must add up
to its clue and may not repeat a digit. The solver precomputes, for each run, every set of
distinct digits with the right size and sum, keeps per-cell candidates as the union of the
digits still possible in both of its runs, and backtracks on the most constrained cell.

    python kakuro.py            # solve the built-in puzzle
    python kakuro.py --random   # fill PATTERN with random digits, derive the clues, solve them back

Grid format: '#' is a black cell, 'D\\R' a clue cell (down sum D, right sum R; either
may be empty), '.' a white cell. Cells are separated by spaces.
"""
from __future__ import annotations

import random
import sys
from functools import lru_cache
from itertools import combinations

PUZZLE = """\
# 11\\ 19\\ # # 30\\ 7\\ 7\\
\\10 . . 35\\ \\11 . . .
\\6 . . . 15\\10 . . .
\\35 . . . . . 30\\ #
# \\20 . . . . . 15\\
# 12\\ 8\\33 . . . . .
\\14 . . . \\14 . . .
\\23 . . . # \\13 . .
"""

# A white/black layout for --random: '.' white, '#' black (clue cells are derived).
PATTERN = """\
# # # # # # # #
# . . # # . . .
# . . . # . . .
# . . . . . # #
# # . . . . . #
# # # . . . . .
# . . . # . . .
# . . . # # . .
"""


@lru_cache(maxsize=None)
def combos(length: int, total: int) -> tuple[frozenset[int], ...]:
    """All sets of `length` distinct digits 1-9 summing to `total`."""
    return tuple(frozenset(c) for c in combinations(range(1, 10), length) if sum(c) == total)


def parse(text: str):
    grid = [line.split() for line in text.strip("\n").split("\n")]
    rows, cols = len(grid), max(len(r) for r in grid)
    for r in grid:
        r += ["#"] * (cols - len(r))
    runs = []  # (total, [cells])
    for r in range(rows):
        for c in range(cols):
            tok = grid[r][c]
            if "\\" not in tok:
                continue
            down, right = tok.split("\\")
            if right:
                cells = []
                k = c + 1
                while k < cols and grid[r][k] == ".":
                    cells.append((r, k))
                    k += 1
                runs.append((int(right), cells))
            if down:
                cells = []
                k = r + 1
                while k < rows and grid[k][c] == ".":
                    cells.append((k, c))
                    k += 1
                runs.append((int(down), cells))
    return grid, runs


def solve(runs):
    cell_runs: dict[tuple[int, int], list[int]] = {}
    for i, (_, cells) in enumerate(runs):
        for cell in cells:
            cell_runs.setdefault(cell, []).append(i)
    values: dict[tuple[int, int], int] = {}

    def candidates(cell) -> set[int]:
        cand = set(range(1, 10))
        for i in cell_runs[cell]:
            total, cells = runs[i]
            used = {values[c] for c in cells if c in values}
            left = total - sum(used)
            empty = len(cells) - len(used)
            possible = set()
            for combo in combos(len(cells), total):
                if used <= combo:
                    possible |= combo - used
            cand &= possible
            if empty == 1:
                cand &= {left}
        return cand

    def search() -> bool:
        free = [c for c in cell_runs if c not in values]
        if not free:
            return True
        best, best_cand = None, None
        for c in free:
            cand = candidates(c)
            if not cand:
                return False
            if best is None or len(cand) < len(best_cand):
                best, best_cand = c, cand
                if len(cand) == 1:
                    break
        for v in sorted(best_cand):
            values[best] = v
            if search():
                return True
            del values[best]
        return False

    return values if search() else None


def show(grid, values) -> str:
    out = []
    for r, row in enumerate(grid):
        line = []
        for c, tok in enumerate(row):
            if tok == ".":
                line.append(f"  {values.get((r, c), '.')}  ")
            elif tok == "#":
                line.append(" ### ")
            else:
                line.append(tok.center(5))
        out.append("".join(line))
    return "\n".join(out)


def verify(runs, values) -> bool:
    for total, cells in runs:
        digits = [values[c] for c in cells]
        if sum(digits) != total or len(set(digits)) != len(digits):
            return False
    return True


def fill_pattern(pattern: str, rng: random.Random):
    """Random digits for every white cell of `pattern` with no repeats inside a run."""
    cells = [line.split() for line in pattern.strip("\n").split("\n")]
    rows, cols = len(cells), len(cells[0])
    whites = [(r, c) for r in range(rows) for c in range(cols) if cells[r][c] == "."]
    values: dict[tuple[int, int], int] = {}

    def run_of(cell, dr, dc):
        r, c = cell
        while 0 <= r - dr and 0 <= c - dc and cells[r - dr][c - dc] == ".":
            r, c = r - dr, c - dc
        out = []
        while r < rows and c < cols and cells[r][c] == ".":
            out.append((r, c))
            r, c = r + dr, c + dc
        return out

    def fill(i: int) -> bool:
        if i == len(whites):
            return True
        cell = whites[i]
        used = {values[x] for x in run_of(cell, 0, 1) + run_of(cell, 1, 0) if x in values}
        digits = [d for d in range(1, 10) if d not in used]
        rng.shuffle(digits)
        for d in digits:
            values[cell] = d
            if fill(i + 1):
                return True
            del values[cell]
        return False

    fill(0)
    # turn black cells next to runs into clue cells
    grid = []
    for r in range(rows):
        row = []
        for c in range(cols):
            if cells[r][c] == ".":
                row.append(".")
                continue
            right = sum(values[x] for x in run_of((r, c + 1), 0, 1)) if c + 1 < cols and cells[r][c + 1] == "." else 0
            down = sum(values[x] for x in run_of((r + 1, c), 1, 0)) if r + 1 < rows and cells[r + 1][c] == "." else 0
            row.append(f"{down or ''}\\{right or ''}" if right or down else "#")
        grid.append(row)
    return "\n".join(" ".join(row) for row in grid), values


def main() -> None:
    if "--random" in sys.argv:
        text, _truth = fill_pattern(PATTERN, random.Random())
        grid, runs = parse(text)
        print("Clues derived from a random filling:")
        print(show(grid, {}))
        print()
    else:
        grid, runs = parse(PUZZLE)
    print(f"{len(runs)} runs, {len({cell for _, cs in runs for cell in cs})} white cells")
    values = solve(runs)
    if values is None:
        print("No solution.")
        return
    print(show(grid, values))
    print("verified" if verify(runs, values) else "BUG: invalid solution")


if __name__ == "__main__":
    main()
