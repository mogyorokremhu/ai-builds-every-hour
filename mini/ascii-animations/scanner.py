#!/usr/bin/env python3
"""Knight-Rider style scanner: a bright head sweeps back and forth with a fading tail.

Usage: python scanner.py [--frames N] [--width 40] [--tail 5] [--fps 25]
"""
import argparse
import sys
import time

SHADES = "@Oo+:. "


def frame(pos, direction, width, tail):
    cells = [" "] * width
    for k in range(tail + 1):
        x = pos - direction * k
        if 0 <= x < width:
            cells[x] = SHADES[min(k, len(SHADES) - 1)]
    return "[" + "".join(cells) + "]"


def positions(width):
    """Yield (pos, direction) forever, bouncing between the edges."""
    pos, d = 0, 1
    while True:
        yield pos, d
        if not 0 <= pos + d < width:
            d = -d
        pos += d


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--frames", type=int, default=0)
    ap.add_argument("--width", type=int, default=40)
    ap.add_argument("--tail", type=int, default=5)
    ap.add_argument("--fps", type=float, default=25)
    a = ap.parse_args()
    gen = positions(a.width)
    n = 0
    try:
        while a.frames == 0 or n < a.frames:
            pos, d = next(gen)
            sys.stdout.write("\r" + frame(pos, d, a.width, a.tail))
            sys.stdout.flush()
            n += 1
            time.sleep(1 / a.fps)
    except KeyboardInterrupt:
        pass
    print()


if __name__ == "__main__":
    main()
