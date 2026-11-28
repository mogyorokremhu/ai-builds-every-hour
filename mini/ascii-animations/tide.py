#!/usr/bin/env python3
"""Tide: a shoreline where waves roll in and out over wet sand.

Usage: python tide.py [--frames N] [--fps 12]
"""
import argparse
import math
import sys
import time

W, H = 70, 16


def frame(t):
    rows = []
    for y in range(H):
        row = ""
        for x in range(W):
            shore = 40 + 14 * math.sin(t * 0.5) + 3 * math.sin(y * 0.6 + t)
            d = x - shore
            if d < -6:
                row += "~" if (x + y + int(t * 3)) % 4 else "-"
            elif d < -2:
                row += "="
            elif d < 0:
                row += "."  # foam
            elif d < 3:
                row += ","  # wet sand
            else:
                row += " " if (x * 7 + y * 13) % 11 else "'"
        rows.append(row)
    return "\n".join(rows)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--frames", type=int, default=200)
    p.add_argument("--fps", type=float, default=12)
    a = p.parse_args()
    for f in range(a.frames):
        sys.stdout.write("\x1b[H\x1b[2J" + frame(f * 0.25) + "\n")
        sys.stdout.flush()
        time.sleep(1 / a.fps)


if __name__ == "__main__":
    main()
