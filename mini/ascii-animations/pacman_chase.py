#!/usr/bin/env python3
"""Pac-Man style chase: a chomper eats dots while a ghost follows it across a row.

Usage: python pacman_chase.py [--fps 10] [--frames N] [--width 40]
"""
import argparse
import sys
import time


def render(t, width):
    pos = t % (width + 6)
    dots = ["." if i % 2 == 0 else " " for i in range(width)]
    for i in range(min(pos, width)):
        dots[i] = " "
    row = dots[:]
    mouth = "C" if t % 2 == 0 else "c"
    if pos < width:
        row[pos] = mouth
    ghost = pos - 4
    if 0 <= ghost < width:
        row[ghost] = "M"
    return "".join(row)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fps", type=float, default=10)
    ap.add_argument("--frames", type=int, default=0)
    ap.add_argument("--width", type=int, default=40)
    a = ap.parse_args()
    t = 0
    while a.frames == 0 or t < a.frames:
        sys.stdout.write("\r" + render(t, a.width) + "  ")
        sys.stdout.flush()
        time.sleep(1 / a.fps)
        t += 1
    print()


if __name__ == "__main__":
    main()
