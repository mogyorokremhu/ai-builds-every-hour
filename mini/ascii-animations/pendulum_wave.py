#!/usr/bin/env python3
"""Pendulum wave: N pendulums of slightly different lengths drift in and out of phase.

Usage: python pendulum_wave.py [--frames N] [--count 15] [--width 61] [--fps 30]
"""
import argparse
import math
import sys
import time


def positions(t, count, width, cycle=60.0, base_swings=30):
    """Pendulum i completes base_swings+i swings per `cycle` seconds; returns columns."""
    mid = (width - 1) / 2
    return [round(mid + mid * math.sin(2 * math.pi * (base_swings + i) * t / cycle)) for i in range(count)]


def render(t, count, width):
    lines = []
    for col in positions(t, count, width):
        row = [" "] * width
        row[(width - 1) // 2] = "|"
        row[col] = "O"
        lines.append("".join(row))
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--frames", type=int, default=0)
    ap.add_argument("--count", type=int, default=15)
    ap.add_argument("--width", type=int, default=61)
    ap.add_argument("--fps", type=float, default=30)
    a = ap.parse_args()
    n = 0
    try:
        while a.frames == 0 or n < a.frames:
            sys.stdout.write("\x1b[H\x1b[2J" + render(n / a.fps, a.count, a.width) + "\n")
            sys.stdout.flush()
            n += 1
            time.sleep(1 / a.fps)
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
