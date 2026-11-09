#!/usr/bin/env python3
"""Bubbles rising and wobbling in a tank; bigger ones rise faster and pop at the surface.

Usage: python bubbles.py [--frames N] [--width 50] [--height 20] [--fps 15] [--seed S]
"""
import argparse
import math
import random
import sys
import time


def step(bubbles, w, h, rng, t):
    if rng.random() < 0.35:
        bubbles.append({"x": rng.uniform(2, w - 3), "y": float(h - 1), "r": rng.choice([0, 1, 2]), "ph": rng.random() * 6.28})
    for b in bubbles:
        b["y"] -= 0.25 + 0.2 * b["r"]
        b["x"] += 0.15 * math.sin(t * 0.4 + b["ph"])
    bubbles[:] = [b for b in bubbles if b["y"] > 0]


def render(bubbles, w, h):
    grid = [[" "] * w for _ in range(h)]
    grid[0] = ["~"] * w
    for b in bubbles:
        x, y = int(round(b["x"])), int(round(b["y"]))
        if 0 < y < h and 0 <= x < w:
            grid[y][x] = ".oO"[b["r"]]
    return "\n".join("".join(r) for r in grid)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--frames", type=int, default=0)
    ap.add_argument("--width", type=int, default=50)
    ap.add_argument("--height", type=int, default=20)
    ap.add_argument("--fps", type=float, default=15)
    ap.add_argument("--seed", type=int, default=None)
    a = ap.parse_args()
    rng = random.Random(a.seed)
    bubbles, n = [], 0
    try:
        while a.frames == 0 or n < a.frames:
            step(bubbles, a.width, a.height, rng, n)
            sys.stdout.write("\x1b[H\x1b[2J" + render(bubbles, a.width, a.height) + "\n")
            sys.stdout.flush()
            n += 1
            time.sleep(1 / a.fps)
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
