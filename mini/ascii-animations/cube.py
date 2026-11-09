#!/usr/bin/env python3
"""Rotating wireframe cube drawn with ASCII lines.

Usage: python cube.py [--frames N] [--size 10] [--fps 20]
"""
import argparse
import math
import sys
import time

VERTS = [(x, y, z) for x in (-1, 1) for y in (-1, 1) for z in (-1, 1)]
EDGES = [(i, j) for i in range(8) for j in range(i + 1, 8)
         if sum(a != b for a, b in zip(VERTS[i], VERTS[j])) == 1]


def project(v, ax, ay, scale, w, h):
    x, y, z = v
    y, z = y * math.cos(ax) - z * math.sin(ax), y * math.sin(ax) + z * math.cos(ax)
    x, z = x * math.cos(ay) + z * math.sin(ay), -x * math.sin(ay) + z * math.cos(ay)
    d = 4 / (4 - z)
    return int(w / 2 + x * scale * 2 * d), int(h / 2 + y * scale * d)


def line(grid, p, q, ch):
    (x0, y0), (x1, y1) = p, q
    n = max(abs(x1 - x0), abs(y1 - y0), 1)
    for i in range(n + 1):
        x = round(x0 + (x1 - x0) * i / n)
        y = round(y0 + (y1 - y0) * i / n)
        if 0 <= y < len(grid) and 0 <= x < len(grid[0]):
            grid[y][x] = ch


def render(ax, ay, size):
    w, h = size * 5, size * 2 + 2
    grid = [[" "] * w for _ in range(h)]
    pts = [project(v, ax, ay, size / 1.6, w, h) for v in VERTS]
    for i, j in EDGES:
        line(grid, pts[i], pts[j], ".")
    for p in pts:
        line(grid, p, p, "#")
    return "\n".join("".join(r) for r in grid)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--frames", type=int, default=0)
    ap.add_argument("--size", type=int, default=10)
    ap.add_argument("--fps", type=float, default=20)
    a = ap.parse_args()
    f = 0
    while a.frames == 0 or f < a.frames:
        sys.stdout.write("\x1b[H\x1b[2J" + render(f * 0.07, f * 0.11, a.size) + "\n")
        sys.stdout.flush()
        time.sleep(1 / a.fps)
        f += 1


if __name__ == "__main__":
    main()
