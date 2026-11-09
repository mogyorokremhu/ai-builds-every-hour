#!/usr/bin/env python3
"""Fly through a tunnel of concentric rings drawn as ASCII.

Usage: python tunnel.py [--frames N] [--width 60] [--height 24] [--fps 20]
"""
import argparse
import math
import sys
import time

SHADES = " .:-=+*#%@"


def frame(t, w, h):
    rows = []
    for y in range(h):
        row = []
        for x in range(w):
            dx, dy = (x - w / 2) / (w / 2), (y - h / 2) / (h / 2) * 0.9
            r = math.hypot(dx, dy) + 1e-6
            ang = math.atan2(dy, dx)
            depth = 1 / r
            v = math.sin(depth * 3 - t * 2) + 0.5 * math.sin(ang * 4 + t)
            k = int((v + 1.5) / 3 * (len(SHADES) - 1))
            if r < 0.08:
                k = 0
            row.append(SHADES[max(0, min(len(SHADES) - 1, k))])
        rows.append("".join(row))
    return "\n".join(rows)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--frames", type=int, default=0)
    ap.add_argument("--width", type=int, default=60)
    ap.add_argument("--height", type=int, default=24)
    ap.add_argument("--fps", type=float, default=20)
    a = ap.parse_args()
    n = 0
    while a.frames == 0 or n < a.frames:
        sys.stdout.write("\x1b[H" + frame(n / a.fps, a.width, a.height) + "\n")
        sys.stdout.flush()
        n += 1
        time.sleep(1 / a.fps)


if __name__ == "__main__":
    main()
