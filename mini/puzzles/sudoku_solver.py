"""Sudoku solver using constraint propagation + backtracking with the MRV heuristic.

Run: python sudoku_solver.py            (solves a built-in hard puzzle)
     python sudoku_solver.py <81 chars> (digits, with 0 or . for blanks)
"""
from __future__ import annotations

import sys

HARD = "8..........36......7..9.2...5...7.......457.....1...3...1....68..85...1..9....4.."


def parse(text: str) -> list[int]:
    cells = [0 if c in ".0" else int(c) for c in text if c in ".0123456789"]
    if len(cells) != 81:
        raise ValueError("a sudoku needs exactly 81 cells")
    return cells


def candidates(grid: list[int], i: int) -> set[int]:
    r, c = divmod(i, 9)
    br, bc = 3 * (r // 3), 3 * (c // 3)
    used = {grid[r * 9 + k] for k in range(9)} | {grid[k * 9 + c] for k in range(9)}
    used |= {grid[(br + a) * 9 + bc + b] for a in range(3) for b in range(3)}
    return set(range(1, 10)) - used


def solve(grid: list[int]) -> list[int] | None:
    """Return a solved copy of ``grid`` or None if it has no solution."""
    grid = grid[:]
    best, best_cands = -1, None
    for i in range(81):
        if grid[i] == 0:
            cands = candidates(grid, i)
            if not cands:
                return None
            if best_cands is None or len(cands) < len(best_cands):
                best, best_cands = i, cands
                if len(cands) == 1:
                    break
    if best_cands is None:
        return grid
    for v in sorted(best_cands):
        grid[best] = v
        result = solve(grid)
        if result:
            return result
    return None


def show(grid: list[int]) -> str:
    lines = []
    for r in range(9):
        if r and r % 3 == 0:
            lines.append("------+-------+------")
        row = [str(grid[r * 9 + c] or ".") for c in range(9)]
        lines.append(" | ".join(" ".join(row[k:k + 3]) for k in (0, 3, 6)))
    return "\n".join(lines)


if __name__ == "__main__":
    puzzle = parse(sys.argv[1] if len(sys.argv) > 1 else HARD)
    print(show(puzzle), "\n")
    solution = solve(puzzle)
    print(show(solution) if solution else "No solution.")
