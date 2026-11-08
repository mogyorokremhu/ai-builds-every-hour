#!/usr/bin/env python3
"""domino_tiling - count domino tilings of an m x n board (broken-profile DP) and print a random one.

  python3 domino_tiling.py 8 8        -> 12988816 tilings, then a random 8x8 tiling
"""
import random
import sys
from functools import lru_cache


def count(m, n):
    if m > n: m, n = n, m
    if (m * n) % 2: return 0

    @lru_cache(None)
    def go(pos, mask):
        # mask: bit i set = cell pos+i already filled (window of m cells, column-major)
        if pos == m * n: return 1 if mask == 0 else 0
        if mask & 1: return go(pos + 1, mask >> 1)
        total = 0
        r = pos % m
        if r + 1 < m and not mask & 2: total += go(pos + 1, (mask | 2) >> 1)  # vertical
        if pos + m < m * n: total += go(pos + 1, (mask | (1 << m)) >> 1)       # horizontal
        return total
    return go(0, 0)


def random_tiling(m, n, rng=random):
    """Rejection-free random tiling by backtracking with shuffled choices (fine for small boards)."""
    grid = [[None] * n for _ in range(m)]
    sym = "─│"

    def solve(k):
        while k < m * n and grid[k // n][k % n] is not None: k += 1
        if k == m * n: return True
        r, c = divmod(k, n)
        opts = []
        if c + 1 < n and grid[r][c + 1] is None: opts.append((r, c + 1))
        if r + 1 < m and grid[r + 1][c] is None: opts.append((r + 1, c))
        rng.shuffle(opts)
        for rr, cc in opts:
            grid[r][c] = grid[rr][cc] = "H" if rr == r else "V"
            if solve(k + 1): return True
            grid[r][c] = grid[rr][cc] = None
        return False

    if not solve(0): return None
    return [["═" if x == "H" else "║" for x in row] for row in grid]


def selftest():
    assert count(2, 2) == 2 and count(2, 3) == 3 and count(3, 3) == 0
    assert count(4, 4) == 36 and count(8, 8) == 12988816
    t = random_tiling(4, 5, random.Random(1)); assert t and all(len(r) == 5 for r in t)
    print("ok")


if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "--selftest": selftest()
    else:
        m, n = (int(x) for x in sys.argv[1:3]) if len(sys.argv) > 2 else (6, 6)
        print(f"{m}x{n}: {count(m, n)} tilings")
        t = random_tiling(m, n)
        if t: print("\n".join("".join(r) for r in t))
