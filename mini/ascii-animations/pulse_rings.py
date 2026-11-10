#!/usr/bin/env python3
"""Pulse rings: concentric expanding rings that fade as they grow.

Usage: python pulse_rings.py [--fps 20] [--frames N] [--period 8]
"""
import argparse
import math
import sys
import time

W, H = 49, 21
SHADES = "@#*+:. "


def render(t, period):
    cx, cy = W // 2, H // 2
    lines = []
    for y in range(H):
        row = ""
        for x in range(W):
            d = math.hypot((x - cx) / 2, y - cy)
            phase = (d - t * 0.5) % period
            # bright just behind each ring front, fading with distance
            k = int(phase / period * len(SHADES))
            fade = d > 9
            ch = SHADES[min(len(SHADES) - 1, k + (2 if fade else 0))]
            row += ch
        lines.append(row)
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fps", type=float, default=20)
    ap.add_argument("--frames", type=int, default=0)
    ap.add_argument("--period", type=float, default=8)
    a = ap.parse_args()
    f = 0
    while a.frames == 0 or f < a.frames:
        sys.stdout.write("\x1b[H\x1b[2J" + render(f, a.period) + "\n")
        sys.stdout.flush()
        time.sleep(1 / a.fps)
        f += 1


if __name__ == "__main__":
    main()
