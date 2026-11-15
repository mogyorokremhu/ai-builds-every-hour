#!/usr/bin/env python3
"""Spiral galaxy: stars orbiting a bright core along rotating spiral arms.

Usage: python spiral_galaxy.py [--fps 15] [--frames N] [--arms 2] [--stars 220] [--seed 1]
"""
import argparse
import math
import random
import sys
import time

W, H = 60, 24


def make_stars(n, arms, rng):
    stars = []
    for _ in range(n):
        r = rng.random() ** 0.7
        arm = rng.randrange(arms)
        ang = arm * 2 * math.pi / arms + r * 4 + rng.gauss(0, 0.25)
        stars.append((r, ang))
    return stars


def render(stars, t):
    grid = [[" "] * W for _ in range(H)]
    for r, ang in stars:
        a = ang + t * 0.05 / (0.2 + r)
        x = int(W / 2 + math.cos(a) * r * (W / 2 - 1))
        y = int(H / 2 + math.sin(a) * r * (H / 2 - 1))
        if 0 <= x < W and 0 <= y < H:
            grid[y][x] = "*" if r < 0.35 else ("+" if r < 0.7 else ".")
    grid[H // 2][W // 2] = "@"
    return "\n".join("".join(row) for row in grid)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fps", type=float, default=15)
    ap.add_argument("--frames", type=int, default=0)
    ap.add_argument("--arms", type=int, default=2)
    ap.add_argument("--stars", type=int, default=220)
    ap.add_argument("--seed", type=int, default=1)
    a = ap.parse_args()
    stars = make_stars(a.stars, a.arms, random.Random(a.seed))
    t = 0
    while a.frames == 0 or t < a.frames:
        sys.stdout.write("\x1b[H\x1b[2J" + render(stars, t) + "\n")
        sys.stdout.flush()
        time.sleep(1 / a.fps)
        t += 1


if __name__ == "__main__":
    main()
