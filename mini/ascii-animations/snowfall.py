#!/usr/bin/env python3
"""Snowfall: flakes drift down with a gentle sideways wind and pile up on the ground.

Usage: python snowfall.py [--frames N] [--width 60] [--height 20] [--fps 12] [--seed S]
"""
import argparse
import math
import random
import sys
import time


def step(flakes, pile, w, h, rng, t):
    if rng.random() < 0.8:
        flakes.append([rng.uniform(0, w), 0.0, rng.choice("*.+"), rng.uniform(0.3, 0.9)])
    wind = math.sin(t / 15) * 0.4
    keep = []
    for f in flakes:
        f[1] += f[3]
        f[0] = (f[0] + wind + rng.uniform(-0.2, 0.2)) % w
        x = int(f[0])
        if f[1] >= h - 1 - pile[x]:
            pile[x] = min(pile[x] + 1, 4)
        else:
            keep.append(f)
    flakes[:] = keep


def render(flakes, pile, w, h):
    grid = [[" "] * w for _ in range(h)]
    for x in range(w):
        for k in range(pile[x] + 1):
            grid[h - 1 - k][x] = "_" if k == 0 else "#"
    for f in flakes:
        grid[int(f[1])][int(f[0])] = f[2]
    return "\n".join("".join(r) for r in grid)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--frames", type=int, default=0)
    ap.add_argument("--width", type=int, default=60)
    ap.add_argument("--height", type=int, default=20)
    ap.add_argument("--fps", type=float, default=12)
    ap.add_argument("--seed", type=int, default=None)
    a = ap.parse_args()
    rng = random.Random(a.seed)
    flakes, pile, n = [], [0] * a.width, 0
    try:
        while a.frames == 0 or n < a.frames:
            step(flakes, pile, a.width, a.height, rng, n)
            sys.stdout.write("\x1b[H\x1b[2J" + render(flakes, pile, a.width, a.height) + "\n")
            sys.stdout.flush()
            n += 1
            time.sleep(1 / a.fps)
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
