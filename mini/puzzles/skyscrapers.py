#!/usr/bin/env python3
"""Skyscrapers puzzle solver.

Fill an N×N grid with building heights 1..N, each once per row and column (a Latin
square). The clues around the edge say how many buildings you can see from that side —
taller buildings hide shorter ones behind them. Solved row by row: every row is chosen
from the permutations that satisfy its left/right clues, with column uniqueness and the
top/bottom clues checked as soon as possible (prefix pruning).

    python skyscrapers.py              # solve the built-in 5×5 puzzle
    python skyscrapers.py --random 6   # generate a fresh 6×6 puzzle from a random solution and solve it
"""
from __future__ import annotations

import random
import sys
from itertools import permutations

# clues: top (left→right), right (top→bottom), bottom (left→right), left (top→bottom); 0 = no clue
PUZZLE_5 = {
    "top": [4, 0, 0, 2, 0],
    "right": [1, 0, 2, 3, 3],
    "bottom": [1, 0, 2, 3, 3],
    "left": [4, 0, 3, 0, 0],
}


def visible(line) -> int:
    """How many buildings can be seen looking along `line` from its start."""
    seen, tallest = 0, 0
    for h in line:
        if h > tallest:
            seen += 1
            tallest = h
    return seen


def max_visible_prefix_ok(prefix, n: int, clue: int) -> bool:
    """Can a column whose first cells are `prefix` still show exactly `clue` from the top?"""
    if not clue:
        return True
    seen = visible(prefix)
    if seen > clue:
        return False
    # the best case adds one building for every remaining height above the current tallest
    tallest = max(prefix)
    return seen + (n - tallest) >= clue and (tallest < n or seen == clue)


def solve(n: int, clues: dict[str, list[int]]):
    rows_ok = []
    for r in range(n):
        left, right = clues["left"][r], clues["right"][r]
        rows_ok.append([p for p in permutations(range(1, n + 1))
                        if (not left or visible(p) == left) and (not right or visible(p[::-1]) == right)])
    grid: list[tuple[int, ...]] = []

    def columns_ok() -> bool:
        k = len(grid)
        for c in range(n):
            col = [row[c] for row in grid]
            if len(set(col)) != k:
                return False
            if not max_visible_prefix_ok(col, n, clues["top"][c]):
                return False
            if k == n:
                if clues["top"][c] and visible(col) != clues["top"][c]:
                    return False
                if clues["bottom"][c] and visible(col[::-1]) != clues["bottom"][c]:
                    return False
        return True

    def search(r: int) -> bool:
        if r == n:
            return True
        for p in rows_ok[r]:
            grid.append(p)
            if columns_ok() and search(r + 1):
                return True
            grid.pop()
        return False

    return [list(row) for row in grid] if search(0) else None


def clues_of(grid) -> dict[str, list[int]]:
    n = len(grid)
    cols = [[grid[r][c] for r in range(n)] for c in range(n)]
    return {
        "top": [visible(c) for c in cols],
        "bottom": [visible(c[::-1]) for c in cols],
        "left": [visible(row) for row in grid],
        "right": [visible(row[::-1]) for row in grid],
    }


def random_latin(n: int, rng: random.Random):
    base = [[(r + c) % n + 1 for c in range(n)] for r in range(n)]
    rng.shuffle(base)
    cols = list(range(n))
    rng.shuffle(cols)
    return [[row[c] for c in cols] for row in base]


def show(grid, clues) -> str:
    n = len(grid) if grid else len(clues["top"])
    fmt = lambda v: str(v) if v else " "
    lines = ["    " + " ".join(fmt(v) for v in clues["top"])]
    lines.append("   +" + "-" * (2 * n - 1) + "+")
    for r in range(n):
        cells = " ".join(str(v) for v in grid[r]) if grid else " ".join("." * n)
        lines.append(f" {fmt(clues['left'][r])} |{cells}| {fmt(clues['right'][r])}")
    lines.append("   +" + "-" * (2 * n - 1) + "+")
    lines.append("    " + " ".join(fmt(v) for v in clues["bottom"]))
    return "\n".join(lines)


def main() -> None:
    if "--random" in sys.argv:
        i = sys.argv.index("--random")
        n = int(sys.argv[i + 1]) if i + 1 < len(sys.argv) else 5
        rng = random.Random()
        clues = clues_of(random_latin(n, rng))
        # hide about a third of the clues to make it a puzzle
        for side in clues:
            clues[side] = [v if rng.random() > 0.35 else 0 for v in clues[side]]
    else:
        n, clues = 5, PUZZLE_5
    print("Puzzle:")
    print(show(None, clues))
    sol = solve(n, clues)
    print("\nSolution:" if sol else "\nNo solution.")
    if sol:
        print(show(sol, clues))
        got = clues_of(sol)
        assert all(not v or v == got[side][i] for side in clues for i, v in enumerate(clues[side]))


if __name__ == "__main__":
    main()
