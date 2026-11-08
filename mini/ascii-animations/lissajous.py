#!/usr/bin/env python3
"""Lissajous curves: x = sin(a·t + phase), y = sin(b·t), drawn with a fading trail in braille dots.

Usage: python lissajous.py [--frames N] [--a 3] [--b 2] [--width 60] [--height 20] [--fps 30]
"""
from __future__ import annotations

import argparse
import math
import sys
import time

BRAILLE_BITS = [[0x01, 0x08], [0x02, 0x10], [0x04, 0x20], [0x40, 0x80]]  # [row][col] within a 2x4 cell


def point(t: float, a: float, b: float, phase: float) -> tuple[float, float]:
    return math.sin(a * t + phase), math.sin(b * t)


def to_cell(x: float, y: float, w: int, h: int) -> tuple[int, int]:
    """Map x,y in [-1,1] to a dot coordinate on a (2w)x(4h) braille grid."""
    return (min(2 * w - 1, int((x + 1) / 2 * 2 * w)), min(4 * h - 1, int((1 - y) / 2 * 4 * h)))


def render(points: list[tuple[float, float]], w: int, h: int) -> str:
    cells = [[0] * w for _ in range(h)]
    for x, y in points:
        dx, dy = to_cell(x, y, w, h)
        cells[dy // 4][dx // 2] |= BRAILLE_BITS[dy % 4][dx % 2]
    return "\n".join("".join(chr(0x2800 + c) for c in row) for row in cells)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--frames", type=int, default=0)
    ap.add_argument("--a", type=float, default=3)
    ap.add_argument("--b", type=float, default=2)
    ap.add_argument("--width", type=int, default=60)
    ap.add_argument("--height", type=int, default=20)
    ap.add_argument("--fps", type=float, default=30)
    ap.add_argument("--trail", type=int, default=400, help="points kept in the trail")
    a = ap.parse_args(argv)
    n = 0
    try:
        sys.stdout.write("\x1b[2J\x1b[?25l")
        while not a.frames or n < a.frames:
            phase = n * 0.03
            pts = [point(phase * 4 + i * 0.015, a.a, a.b, phase) for i in range(a.trail)]
            sys.stdout.write("\x1b[H" + render(pts, a.width, a.height) + f"\na={a.a:g} b={a.b:g} phase={phase % (2 * math.pi):.2f}\n")
            sys.stdout.flush()
            time.sleep(1 / a.fps)
            n += 1
    except KeyboardInterrupt:
        pass
    finally:
        sys.stdout.write("\x1b[?25h\n")


if __name__ == "__main__":
    main()
