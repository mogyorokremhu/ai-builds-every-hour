"""Spiral matrix: generate an n x n spiral and read a matrix in spiral order.

Usage: python spiral_matrix.py [n]
"""
import sys


def make(n):
    g = [[0] * n for _ in range(n)]
    r = c = 0
    dr, dc = 0, 1
    for k in range(1, n * n + 1):
        g[r][c] = k
        nr, nc = r + dr, c + dc
        if not (0 <= nr < n and 0 <= nc < n and g[nr][nc] == 0):
            dr, dc = dc, -dr
            nr, nc = r + dr, c + dc
        r, c = nr, nc
    return g


def read(g):
    out = []
    while g:
        out += g[0]
        g = [list(row) for row in zip(*g[1:])][::-1]
    return out


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    g = make(n)
    w = len(str(n * n))
    for row in g:
        print(" ".join(str(v).rjust(w) for v in row))
    assert read(g) == list(range(1, n * n + 1))
