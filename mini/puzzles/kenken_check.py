#!/usr/bin/env python3
"""kenken_check - tiny KenKen (4x4) solver: cages of (cells, op, target), backtracking.

  python3 kenken_check.py     solves a built-in 4x4 puzzle
"""
from itertools import permutations
from math import prod

N = 4
CAGES = [([(0, 0), (1, 0)], "+", 3), ([(0, 1), (0, 2)], "-", 1), ([(0, 3), (1, 3)], "*", 4),
         ([(1, 1), (1, 2)], "+", 7), ([(2, 0), (3, 0)], "-", 1), ([(2, 1), (3, 1)], "+", 5),
         ([(2, 2), (2, 3)], "*", 2), ([(3, 2), (3, 3)], "-", 1)]


def ok(vals, op, t):
    if op == "+":
        return sum(vals) == t
    if op == "*":
        return prod(vals) == t
    return abs(vals[0] - vals[1]) == t


def solve():
    rows = list(permutations(range(1, N + 1)))

    def rec(grid):
        r = len(grid)
        if r == N:
            return grid
        for row in rows:
            if any(row[c] == g[c] for g in grid for c in range(N)):
                continue
            g2 = grid + [row]
            good = True
            for cells, op, t in CAGES:
                if all(rr <= r for rr, _ in cells):
                    if not ok([g2[rr][cc] for rr, cc in cells], op, t):
                        good = False
                        break
            if good and (res := rec(g2)):
                return res

    return rec([])


if __name__ == "__main__":
    g = solve()
    print("\n".join(" ".join(map(str, r)) for r in g) if g else "no solution")
