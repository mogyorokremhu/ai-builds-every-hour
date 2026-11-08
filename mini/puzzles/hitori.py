#!/usr/bin/env python3
"""hitori - solve Hitori: shade cells so no number repeats in a row/column,
shaded cells never touch orthogonally, and all unshaded cells stay connected.

  python3 hitori.py          solves a built-in 5x5 puzzle
"""
import sys

PUZZLE = ["24135", "13425", "45213", "21544", "35312"]


def solve(grid):
    n = len(grid)
    shaded = [[False] * n for _ in range(n)]

    def connected():
        cells = [(r, c) for r in range(n) for c in range(n) if not shaded[r][c]]
        if not cells: return False
        seen, stack = {cells[0]}, [cells[0]]
        while stack:
            r, c = stack.pop()
            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                p = (r + dr, c + dc)
                if 0 <= p[0] < n and 0 <= p[1] < n and not shaded[p[0]][p[1]] and p not in seen:
                    seen.add(p); stack.append(p)
        return len(seen) == len(cells)

    def dup_ok():
        for i in range(n):
            for line in ([(i, j) for j in range(n)], [(j, i) for j in range(n)]):
                vals = [grid[r][c] for r, c in line if not shaded[r][c]]
                if len(vals) != len(set(vals)): return False
        return True

    def conflicts(r, c):  # a cell must be shaded if it duplicates something and is not rescued
        return any(grid[r][c] == grid[r][j] for j in range(n) if j != c) or \
               any(grid[r][c] == grid[i][c] for i in range(n) if i != r)

    def rec(k):
        if k == n * n: return dup_ok() and connected()
        r, c = divmod(k, n)
        # prune: rows/cols fully decided behind us must be duplicate-free
        for shade in (False, True):
            if shade and not conflicts(r, c): continue
            if shade and ((r and shaded[r - 1][c]) or (c and shaded[r][c - 1])): continue
            shaded[r][c] = shade
            ok = True
            if c == n - 1 or r == n - 1:
                ok = _partial_ok(grid, shaded, r, c, n)
            if ok and rec(k + 1): return True
            shaded[r][c] = False
        return False

    return shaded if rec(0) else None


def _partial_ok(grid, shaded, r, c, n):
    if c == n - 1:
        vals = [grid[r][j] for j in range(n) if not shaded[r][j]]
        if len(vals) != len(set(vals)): return False
    if r == n - 1:
        vals = [grid[i][c] for i in range(n) if not shaded[i][c]]
        if len(vals) != len(set(vals)): return False
    return True


def show(grid, shaded):
    return "\n".join("".join("#" if shaded[r][c] else grid[r][c] for c in range(len(grid))) for r in range(len(grid)))


def selftest():
    g = [[int(ch) for ch in row] for row in PUZZLE]
    s = solve(g)
    assert s is not None
    for r in range(5):
        for c in range(5):
            if s[r][c]:
                assert not (r < 4 and s[r + 1][c]) and not (c < 4 and s[r][c + 1])
    print("ok")


if __name__ == "__main__":
    if "--selftest" in sys.argv: selftest(); sys.exit()
    g = [[int(ch) for ch in row] for row in PUZZLE]
    s = solve(g)
    print(show([[str(x) for x in r] for r in g], s) if s else "no solution")
