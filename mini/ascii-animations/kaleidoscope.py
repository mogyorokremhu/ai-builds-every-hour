#!/usr/bin/env python3
"""Kaleidoscope: drifting coloured specks mirrored into a 4-fold symmetric pattern.

Usage: python kaleidoscope.py [--frames N] [--size S] [--fps F] [--specks N] [--seed S] [--no-color]
Specks move in one quadrant and are reflected across both axes.
"""
from __future__ import annotations

import argparse
import math
import random
import time

PALETTE = [196, 202, 208, 214, 220, 226, 118, 46, 51, 39, 27, 93, 129, 201]


def render(specks: list[list[float]], half: int, color: bool) -> str:
    """Draw specks in a (2*half)x(2*half) grid with mirror symmetry."""
    n = 2 * half
    grid = [[None] * n for _ in range(n)]
    for x, y, _, _, c in specks:
        xi, yi = int(x) % half, int(y) % half
        for gx in (half + xi, half - 1 - xi):
            for gy in (half + yi, half - 1 - yi):
                grid[gy][gx] = int(c)
    out = []
    for row in grid:
        line = ""
        for c in row:
            if c is None:
                line += "  "
            elif color:
                line += f"\x1b[38;5;{PALETTE[c % len(PALETTE)]}m██\x1b[0m"
            else:
                line += "##"
        out.append(line)
    return "\n".join(out)


def step(specks: list[list[float]], half: int, t: float) -> None:
    for s in specks:
        s[2] += math.sin(t + s[4]) * 0.05
        s[3] += math.cos(t * 0.7 + s[4]) * 0.05
        s[0] = (s[0] + s[2]) % half
        s[1] = (s[1] + s[3]) % half
        s[2] *= 0.98
        s[3] *= 0.98


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--frames", type=int, default=0)
    ap.add_argument("--size", type=int, default=12)
    ap.add_argument("--fps", type=float, default=15)
    ap.add_argument("--specks", type=int, default=14)
    ap.add_argument("--seed", type=int, default=None)
    ap.add_argument("--no-color", action="store_true")
    a = ap.parse_args()
    rng = random.Random(a.seed)
    specks = [[rng.uniform(0, a.size), rng.uniform(0, a.size), rng.uniform(-.5, .5),
               rng.uniform(-.5, .5), rng.randrange(len(PALETTE))] for _ in range(a.specks)]
    frame = 0
    try:
        while a.frames == 0 or frame < a.frames:
            step(specks, a.size, frame * 0.1)
            print("\x1b[H" + render(specks, a.size, not a.no_color), flush=True)
            frame += 1
            time.sleep(1 / a.fps)
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
