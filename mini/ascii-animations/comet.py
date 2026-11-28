#!/usr/bin/env python3
"""Comet: a comet on an elliptical orbit around a sun, with a tail pointing away from it.

Usage: python comet.py [--frames N] [--fps 20]
"""
import argparse
import math
import sys
import time

W, H = 72, 24
TAIL = " .:*"


def pos(t):
    """Comet position on an ellipse (sun at the right focus-ish centre)."""
    return 30 * math.cos(t), 9 * math.sin(t)


def frame(t):
    grid = [[" "] * W for _ in range(H)]

    def put(x, y, ch):
        cx, cy = int(round(W / 2 + x)), int(round(H / 2 + y))
        if 0 <= cx < W and 0 <= cy < H:
            grid[cy][cx] = ch

    put(0, 0, "O")
    px, py = pos(t)
    dist = math.hypot(px, py * 2.5) or 1
    length = max(2, int(24 - dist * 0.6))  # tail is longer near the sun
    ux, uy = px / dist, py / dist
    for i in range(length, 0, -1):
        put(px + ux * i, py + uy * i * 0.5, TAIL[min(3, 1 + i * 3 // (length + 1))])
    put(px, py, "@")
    return "\n".join("".join(r) for r in grid)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--frames", type=int, default=300)
    p.add_argument("--fps", type=float, default=20)
    a = p.parse_args()
    for f in range(a.frames):
        sys.stdout.write("\x1b[H\x1b[2J" + frame(f * 0.06) + "\n")
        sys.stdout.flush()
        time.sleep(1 / a.fps)


if __name__ == "__main__":
    main()
