#!/usr/bin/env python3
"""Latin squares: complete a partial square by backtracking, or count/print reduced squares.

usage: latin_square.py N                 print a random Latin square of order N
       latin_square.py --count N         number of reduced Latin squares (N<=6)
       latin_square.py --solve "1.. ..2 .1."  complete a partial square (rows separated by spaces, . = empty)
"""
import random
import sys


def solve(grid, n, rng=None):
    rows = [set() for _ in range(n)]
    cols = [set() for _ in range(n)]
    for r in range(n):
        for c in range(n):
            v = grid[r][c]
            if v:
                if v in rows[r] or v in cols[c]:
                    return None
                rows[r].add(v)
                cols[c].add(v)

    def best():
        pick, opts = None, None
        for r in range(n):
            for c in range(n):
                if not grid[r][c]:
                    o = [v for v in range(1, n + 1) if v not in rows[r] and v not in cols[c]]
                    if pick is None or len(o) < len(opts):
                        pick, opts = (r, c), o
                        if len(o) <= 1:
                            return pick, opts
        return pick, opts

    def go():
        pick, opts = best()
        if pick is None:
            return True
        r, c = pick
        if rng:
            rng.shuffle(opts)
        for v in opts:
            grid[r][c] = v
            rows[r].add(v)
            cols[c].add(v)
            if go():
                return True
            grid[r][c] = 0
            rows[r].discard(v)
            cols[c].discard(v)
        return False

    return grid if go() else None


def count_reduced(n):
    """Reduced squares have first row and column 1..n in order."""
    grid = [[0] * n for _ in range(n)]
    for i in range(n):
        grid[0][i] = i + 1
        grid[i][0] = i + 1
    total = 0

    def go(pos):
        nonlocal total
        if pos == n * n:
            total += 1
            return
        r, c = divmod(pos, n)
        if r == 0 or c == 0:
            return go(pos + 1)
        for v in range(1, n + 1):
            if all(grid[r][k] != v for k in range(c)) and all(grid[k][c] != v for k in range(r)):
                grid[r][c] = v
                go(pos + 1)
                grid[r][c] = 0

    go(0)
    return total


def parse(text):
    rows = text.split()
    n = len(rows)
    return [[0 if ch == "." else int(ch) for ch in row] for row in rows], n


def show(grid):
    return "\n".join(" ".join(map(str, row)) for row in grid)


def main(argv):
    if len(argv) >= 2 and argv[0] == "--count":
        print(count_reduced(int(argv[1])))
    elif len(argv) >= 2 and argv[0] == "--solve":
        grid, n = parse(argv[1])
        res = solve(grid, n)
        print(show(res) if res else "no solution")
    else:
        n = int(argv[0]) if argv else 5
        print(show(solve([[0] * n for _ in range(n)], n, random.Random())))


if __name__ == "__main__":
    main(sys.argv[1:])
