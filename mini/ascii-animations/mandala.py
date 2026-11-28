#!/usr/bin/env python3
"""Mandala: a rotating shape with N-fold radial symmetry that breathes.

Usage: python mandala.py [--frames N] [--fps 15] [--folds 8]
"""
import argparse
import math
import sys
import time

W, H = 61, 29
SHADES = " .:-=+*#%@"


def frame(t, folds):
    rows = []
    for y in range(H):
        row = ""
        for x in range(W):
            dx, dy = (x - W // 2) / 2.0, y - H // 2  # chars are ~2x taller than wide
            r = math.hypot(dx, dy)
            a = math.atan2(dy, dx) + t * 0.3
            petal = abs(math.cos(folds * a / 2))
            ring = 0.5 + 0.5 * math.sin(r * 0.9 - t * 2)
            edge = 11 + 2 * math.sin(t)
            v = petal * ring * max(0.0, 1 - r / edge)
            row += SHADES[min(len(SHADES) - 1, int(v * len(SHADES) * 1.3))]
        rows.append(row)
    return "\n".join(rows)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--frames", type=int, default=200)
    p.add_argument("--fps", type=float, default=15)
    p.add_argument("--folds", type=int, default=8)
    a = p.parse_args()
    for f in range(a.frames):
        sys.stdout.write("\x1b[H\x1b[2J" + frame(f * 0.1, a.folds) + "\n")
        sys.stdout.flush()
        time.sleep(1 / a.fps)


if __name__ == "__main__":
    main()
