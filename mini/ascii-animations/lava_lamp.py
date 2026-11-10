#!/usr/bin/env python3
"""Lava lamp: metaball blobs drift up and down inside a glass tube.

Usage: python lava_lamp.py [--blobs 4] [--fps 15] [--frames N] [--seed S]
"""
import argparse
import math
import random
import sys
import time

W, H = 24, 20
SHADES = " .:-=+*#%@"


def field(blobs, x, y):
    """Sum of r^2 / d^2 influence of every blob at a cell (y is stretched for char aspect)."""
    total = 0.0
    for bx, by, r, _ in blobs:
        d2 = (x - bx) ** 2 + ((y - by) * 2) ** 2 + 0.01
        total += r * r / d2
    return total


def step(blobs, dt=1.0):
    for b in blobs:
        b[1] += b[3] * dt
        if b[1] < 3 or b[1] > H - 3:
            b[3] = -b[3]
            b[1] = max(3, min(H - 3, b[1]))


def render(blobs):
    lines = []
    for y in range(H):
        row = ""
        for x in range(W):
            v = field(blobs, x, y)
            row += SHADES[min(len(SHADES) - 1, int(v * 4))] if v > 0.6 else " "
        lines.append("|" + row + "|")
    return "\n".join(lines) + "\n+" + "-" * W + "+"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--blobs", type=int, default=4)
    ap.add_argument("--fps", type=float, default=15)
    ap.add_argument("--frames", type=int, default=0)
    ap.add_argument("--seed", type=int, default=None)
    a = ap.parse_args()
    rng = random.Random(a.seed)
    blobs = [[rng.uniform(5, W - 5), rng.uniform(4, H - 4), rng.uniform(2.0, 3.5),
              rng.choice((-1, 1)) * rng.uniform(0.15, 0.45)] for _ in range(a.blobs)]
    f = 0
    while a.frames == 0 or f < a.frames:
        step(blobs)
        sys.stdout.write("\x1b[H\x1b[2J" + render(blobs) + "\n")
        sys.stdout.flush()
        time.sleep(1 / a.fps)
        f += 1


if __name__ == "__main__":
    main()
