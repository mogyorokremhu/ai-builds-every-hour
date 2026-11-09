#!/usr/bin/env python3
"""A swinging metronome arm with a tick marker.

Usage: python metronome.py [--frames N] [--bpm 90] [--fps 25]
"""
import argparse
import math
import sys
import time


def render(t, bpm, h=12):
    phase = math.sin(math.pi * t * bpm / 60)  # -1..1, one swing per beat
    w = h * 4 + 1
    grid = [[" "] * w for _ in range(h + 2)]
    cx = w // 2
    for r in range(h):
        x = cx + round(phase * r * 1.4 * 1.5)
        grid[h - r][x] = "|" if abs(phase) < 0.12 else ("/" if phase > 0 else "\\")
    grid[0][cx + round(phase * h * 2.1)] = "O"
    grid[h + 1] = list(("_" * w))
    tick = "TICK" if abs(phase) > 0.97 else "    "
    return "\n".join("".join(r) for r in grid) + f"\n{bpm} bpm  {tick}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--frames", type=int, default=0)
    ap.add_argument("--bpm", type=float, default=90)
    ap.add_argument("--fps", type=float, default=25)
    a = ap.parse_args()
    f = 0
    while a.frames == 0 or f < a.frames:
        sys.stdout.write("\x1b[H\x1b[2J" + render(f / a.fps, a.bpm) + "\n")
        sys.stdout.flush()
        time.sleep(1 / a.fps)
        f += 1


if __name__ == "__main__":
    main()
