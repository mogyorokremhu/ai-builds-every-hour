#!/usr/bin/env python3
"""Planets orbiting a sun; inner planets move faster (Kepler-ish T ~ r^1.5).

Usage: python orbits.py [--frames N] [--planets 4] [--fps 20]
"""
import argparse
import math
import sys
import time

W, H = 61, 25


def frame(t, planets):
    grid = [[" "] * W for _ in range(H)]
    cx, cy = W // 2, H // 2
    for i in range(planets):
        r = 4 + i * 3
        for k in range(72):
            a = k * math.tau / 72
            x, y = int(round(cx + math.cos(a) * r * 2)), int(round(cy + math.sin(a) * r * 0.9))
            if 0 <= x < W and 0 <= y < H:
                grid[y][x] = "."
    grid[cy][cx] = "@"
    for i in range(planets):
        r = 4 + i * 3
        a = t * 1.5 / (r ** 1.5) * 8
        x, y = int(round(cx + math.cos(a) * r * 2)), int(round(cy + math.sin(a) * r * 0.9))
        if 0 <= x < W and 0 <= y < H:
            grid[y][x] = "o0O#"[i % 4]
    return "\n".join("".join(r) for r in grid)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--frames", type=int, default=0)
    ap.add_argument("--planets", type=int, default=4)
    ap.add_argument("--fps", type=float, default=20)
    a = ap.parse_args()
    t = n = 0
    try:
        while a.frames == 0 or n < a.frames:
            sys.stdout.write("\x1b[H\x1b[2J" + frame(t, a.planets) + "\n")
            sys.stdout.flush()
            t += 1
            n += 1
            time.sleep(1 / a.fps)
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
