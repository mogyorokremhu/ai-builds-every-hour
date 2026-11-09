#!/usr/bin/env python3
"""Abelian sandpile: drop grains at the centre and watch it topple into a pattern.

Usage: python sandpile.py [--frames N] [--size 15] [--grains 4] [--fps 20]
"""
import argparse
import sys
import time

SHADES = " .:*#"


def topple(g):
    """One parallel toppling step; returns True if anything moved."""
    n = len(g)
    moved = False
    add = [[0] * n for _ in range(n)]
    for y in range(n):
        for x in range(n):
            if g[y][x] >= 4:
                moved = True
                g[y][x] -= 4
                for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    if 0 <= y + dy < n and 0 <= x + dx < n:
                        add[y + dy][x + dx] += 1
    for y in range(n):
        for x in range(n):
            g[y][x] += add[y][x]
    return moved


def render(g):
    return "\n".join("".join(SHADES[min(c, 4)] * 2 for c in row) for row in g)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--frames", type=int, default=0)
    ap.add_argument("--size", type=int, default=15)
    ap.add_argument("--grains", type=int, default=4)
    ap.add_argument("--fps", type=float, default=20)
    a = ap.parse_args()
    g = [[0] * a.size for _ in range(a.size)]
    c = a.size // 2
    f = 0
    while a.frames == 0 or f < a.frames:
        g[c][c] += a.grains
        topple(g)
        sys.stdout.write("\x1b[H\x1b[2J" + render(g) + f"\ngrains: {(f + 1) * a.grains}\n")
        sys.stdout.flush()
        time.sleep(1 / a.fps)
        f += 1


if __name__ == "__main__":
    main()
