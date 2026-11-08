#!/usr/bin/env python3
"""Scrolling ocean: layered sine waves with parallax, foam crests and a moon (256-colour).

Usage: python waves.py [--frames N] [--width 70] [--height 22] [--fps 30] [--seed S] [--no-color]
"""
from __future__ import annotations

import argparse
import math
import random
import sys
import time

LAYERS = [(0.30, 0.10, 0.9, 24), (0.10, 0.18, -1.3, 25), (0.07, 0.30, 1.8, 26), (0.05, 0.45, -2.4, 27)]  # (amp, base-offset, speed, color)


def init(w, h, rng):
    return {"t": 0.0, "stars": [(rng.randrange(w), rng.randrange(max(1, h // 3))) for _ in range(w // 4)]}


def step(st, w, h, rng):
    st["t"] += 0.12


def surface(layer, x, t, h):
    amp, base, speed, _ = layer
    top = h * (0.45 + base * 1.2)
    return top + amp * h * 0.3 * math.sin(x * 0.18 + t * speed) + amp * h * 0.15 * math.sin(x * 0.47 - t * speed * 0.7)


def render(st, w, h, color):
    t = st["t"]
    grid = [[(" ", None)] * w for _ in range(h)]
    for sx, sy in st["stars"]:
        if (sx + int(t * 3)) % 7:
            grid[sy][sx] = (".", 250)
    mx, my = int(w * 0.75), 2
    for dy in range(-1, 2):
        for dx in range(-2, 3):
            if 0 <= my + dy < h and 0 <= mx + dx < w and dx * dx / 4 + dy * dy <= 1.2:
                grid[my + dy][mx + dx] = ("@", 230)
    for layer in LAYERS:
        for x in range(w):
            top = surface(layer, x, t, h)
            for y in range(max(0, int(top)), h):
                crest = y == int(top)
                if crest:
                    grid[y][x] = ("~", 255)
                elif y == int(top) + 1:
                    grid[y][x] = ("≈", layer[3] + 6)
                else:
                    grid[y][x] = ("░", layer[3])
    out = []
    for row in grid:
        out.append("".join((f"\x1b[38;5;{c}m{ch}" if color and c is not None else "") + ch for ch, c in row) + ("\x1b[0m" if color else ""))
    return "\n".join(out)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--frames", type=int, default=0)
    ap.add_argument("--width", type=int, default=70)
    ap.add_argument("--height", type=int, default=22)
    ap.add_argument("--fps", type=float, default=30)
    ap.add_argument("--seed", type=int, default=None)
    ap.add_argument("--no-color", action="store_true")
    a = ap.parse_args(argv)
    rng = random.Random(a.seed)
    st = init(a.width, a.height, rng)
    n = 0
    try:
        sys.stdout.write("\x1b[2J\x1b[?25l")
        while not a.frames or n < a.frames:
            sys.stdout.write("\x1b[H" + render(st, a.width, a.height, not a.no_color) + "\n")
            sys.stdout.flush()
            step(st, a.width, a.height, rng)
            time.sleep(1 / a.fps)
            n += 1
    except KeyboardInterrupt:
        pass
    finally:
        sys.stdout.write("\x1b[?25h\n")


if __name__ == "__main__":
    main()
