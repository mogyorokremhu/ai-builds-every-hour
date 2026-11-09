#!/usr/bin/env python3
"""Radar sweep: a rotating beam lights up blips that then fade.

Usage: python radar.py [--frames N] [--size 11] [--blips 8] [--seed 1] [--fps 15]
"""
import argparse
import math
import random
import sys
import time

FADE = "@O+:. "


def render(size, angle, blips, ages):
    w, h = size * 4 + 1, size * 2 + 1
    grid = [[" "] * w for _ in range(h)]
    for t in range(0, 360, 6):
        a = math.radians(t)
        for r in range(size + 1):
            x = int(round(size * 2 + math.cos(a) * r * 2))
            y = int(round(size - math.sin(a) * r))
            if 0 <= x < w and 0 <= y < h and (r == size and grid[y][x] == " "):
                grid[y][x] = "."
    for r in range(size + 1):
        x = int(round(size * 2 + math.cos(angle) * r * 2))
        y = int(round(size - math.sin(angle) * r))
        grid[y][x] = "*"
    for (bx, by), age in zip(blips, ages):
        if age < len(FADE):
            grid[by][bx] = FADE[age]
    return "\n".join("".join(r) for r in grid)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--frames", type=int, default=0)
    ap.add_argument("--size", type=int, default=11)
    ap.add_argument("--blips", type=int, default=8)
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--fps", type=float, default=15)
    a = ap.parse_args()
    rng = random.Random(a.seed)
    s = a.size
    blips = []
    for _ in range(a.blips):
        r, t = rng.uniform(2, s - 1), rng.uniform(0, 2 * math.pi)
        blips.append((int(round(s * 2 + math.cos(t) * r * 2)), int(round(s - math.sin(t) * r))))
    ages = [99] * len(blips)
    angle, n = 0.0, 0
    try:
        while a.frames == 0 or n < a.frames:
            for i, (bx, by) in enumerate(blips):
                ba = math.atan2(s - by, (bx - s * 2) / 2) % (2 * math.pi)
                if abs((ba - angle + math.pi) % (2 * math.pi) - math.pi) < 0.2:
                    ages[i] = 0
                else:
                    ages[i] += 1
            sys.stdout.write("\x1b[H\x1b[2J" + render(s, angle % (2 * math.pi), blips, ages) + "\n")
            sys.stdout.flush()
            angle -= 0.15
            n += 1
            time.sleep(1 / a.fps)
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
