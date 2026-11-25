#!/usr/bin/env python3
"""A windmill with four rotating sails on a grassy hill; wind speed varies slowly.

Usage: python windmill.py [--frames N] [--width W] [--height H] [--fps F] [--speed S]
"""
from __future__ import annotations

import argparse
import math
import time


def frame(width: int, height: int, angle: float) -> str:
    """Render one frame: sails are four spokes from the hub, drawn with Bresenham-ish sampling."""
    g = [[" "] * width for _ in range(height)]
    cx, cy = width // 2, height // 3
    for x in range(width):  # hill
        top = height - 4 + int(2 * math.cos(x / 9))
        for y in range(max(top, 0), height):
            g[y][x] = "^" if y == top else "."
    for y in range(cy + 1, height - 3):  # tower, tapering
        half = 2 + (y - cy) // 4
        for x in range(cx - half, cx + half + 1):
            if 0 <= x < width:
                g[y][x] = "#" if x in (cx - half, cx + half) else "|"
    for k in range(4):
        a = angle + k * math.pi / 2
        for r in range(1, 11):
            x, y = cx + round(r * 2 * math.cos(a)), cy + round(r * math.sin(a))
            if 0 <= x < width and 0 <= y < height:
                g[y][x] = "=" if r > 3 else "+"
    g[cy][cx] = "O"
    return "\n".join("".join(r) for r in g)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--frames", type=int, default=0)
    ap.add_argument("--width", type=int, default=60)
    ap.add_argument("--height", type=int, default=20)
    ap.add_argument("--fps", type=float, default=15)
    ap.add_argument("--speed", type=float, default=0.15)
    a = ap.parse_args()
    angle, n = 0.0, 0
    try:
        while a.frames == 0 or n < a.frames:
            angle += a.speed * (1 + 0.6 * math.sin(n / 40))
            print("\x1b[H" + frame(a.width, a.height, angle), flush=True)
            n += 1
            time.sleep(1 / a.fps)
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
