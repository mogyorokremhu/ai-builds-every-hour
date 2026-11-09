#!/usr/bin/env python3
"""Rain on a window: drops fall, splash at the bottom and ripple into a puddle line.

Usage: python rain.py [--frames N] [--width 60] [--height 20] [--fps 20] [--seed S]
"""
import argparse
import random
import sys
import time


def step(drops, splashes, w, h, rng, density):
    for _ in range(int(w * density) + (1 if rng.random() < (w * density) % 1 else 0)):
        drops.append([rng.randrange(w), 0.0, rng.uniform(0.6, 1.4)])
    for d in drops:
        d[1] += d[2]
    landed = [d for d in drops if d[1] >= h - 2]
    drops[:] = [d for d in drops if d[1] < h - 2]
    for d in landed:
        splashes.append([d[0], 0])
    for s in splashes:
        s[1] += 1
    splashes[:] = [s for s in splashes if s[1] < 4]


def render(drops, splashes, w, h):
    grid = [[" "] * w for _ in range(h)]
    for x in range(w):
        grid[h - 1][x] = "~"
    for x, y, _ in drops:
        grid[int(y)][x] = "|"
    for x, age in splashes:
        row = grid[h - 2]
        row[x] = "o" if age < 2 else "."
        for dx in range(1, age + 1):
            for xx in (x - dx, x + dx):
                if 0 <= xx < w and age > 0:
                    row[xx] = "-" if age == dx else row[xx]
    return "\n".join("".join(r) for r in grid)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--frames", type=int, default=0)
    ap.add_argument("--width", type=int, default=60)
    ap.add_argument("--height", type=int, default=20)
    ap.add_argument("--fps", type=float, default=20)
    ap.add_argument("--seed", type=int, default=None)
    a = ap.parse_args()
    rng = random.Random(a.seed)
    drops, splashes, n = [], [], 0
    try:
        while a.frames == 0 or n < a.frames:
            step(drops, splashes, a.width, a.height, rng, 0.15)
            sys.stdout.write("\x1b[H\x1b[2J" + render(drops, splashes, a.width, a.height) + "\n")
            sys.stdout.flush()
            n += 1
            time.sleep(1 / a.fps)
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
