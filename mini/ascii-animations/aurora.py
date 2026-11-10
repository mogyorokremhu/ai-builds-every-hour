#!/usr/bin/env python3
"""Aurora: drifting curtains of light drawn with layered sine waves.

Usage: python aurora.py [--frames N] [--fps 15]
"""
import argparse
import math
import sys
import time

W, H = 70, 18
SHADES = " .:-=+*#%@"


def frame(t):
    rows = []
    for y in range(H):
        row = ""
        for x in range(W):
            v = math.sin(x * 0.12 + t * 0.7) + math.sin(x * 0.05 - t * 0.4 + y * 0.15)
            band = math.exp(-((y - (6 + 3 * math.sin(x * 0.08 + t * 0.3))) ** 2) / 8)
            i = int(max(0, min(0.999, (v + 2) / 4 * band * 1.4)) * len(SHADES))
            row += SHADES[i]
        rows.append(row)
    return "\n".join(rows)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--frames", type=int, default=200)
    p.add_argument("--fps", type=float, default=15)
    a = p.parse_args()
    for f in range(a.frames):
        sys.stdout.write("\x1b[H\x1b[2J" + frame(f * 0.2) + "\n")
        sys.stdout.flush()
        time.sleep(1 / a.fps)


if __name__ == "__main__":
    main()
