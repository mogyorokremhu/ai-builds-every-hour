#!/usr/bin/env python3
"""Raindrops on a pond: the 2D wave equation on a grid, shaded with characters and blues.

Usage: python ripples.py [--frames N] [--width W] [--height H] [--fps F] [--rain P]
                         [--damping D] [--seed S] [--no-color]
Each drop pushes the surface down; waves spread, interfere, reflect off the banks and fade.
"""
from __future__ import annotations

import argparse
import random
import sys
import time

SHADES = " .,:;=+*#%@"
BLUES = [17, 18, 19, 20, 25, 26, 32, 38, 44, 51, 123, 195, 231]


def step(cur: list[list[float]], prev: list[list[float]], damping: float) -> list[list[float]]:
    """One leapfrog step of the damped wave equation (classic two-buffer ripple algorithm).

    new = (sum of 4 neighbours) / 2 − previous, then damped. Edges are fixed (reflect).
    Returns the new height field; the caller rotates buffers.
    """
    h, w = len(cur), len(cur[0])
    nxt = [[0.0] * w for _ in range(h)]
    for y in range(1, h - 1):
        row_u, row, row_d, prow, out = cur[y - 1], cur[y], cur[y + 1], prev[y], nxt[y]
        for x in range(1, w - 1):
            out[x] = ((row_u[x] + row_d[x] + row[x - 1] + row[x + 1]) / 2 - prow[x]) * damping
    return nxt


def drop(field: list[list[float]], x: int, y: int, strength: float, radius: int = 1) -> None:
    """Push the surface down in a small disc around (x, y)."""
    h, w = len(field), len(field[0])
    for dy in range(-radius, radius + 1):
        for dx in range(-radius * 2, radius * 2 + 1):  # cells are ~2:1, so widen the disc
            if (dx / 2) ** 2 + dy * dy <= radius * radius and 0 < x + dx < w - 1 and 0 < y + dy < h - 1:
                field[y + dy][x + dx] -= strength


def render(field: list[list[float]], color: bool) -> str:
    """Shade by the surface slope (fake lighting from the upper left) plus the height."""
    h, w = len(field), len(field[0])
    lines = []
    for y in range(h):
        parts = []
        for x in range(w):
            sx = field[y][min(w - 1, x + 1)] - field[y][max(0, x - 1)]
            sy = field[min(h - 1, y + 1)][x] - field[max(0, y - 1)][x]
            light = max(0.0, min(0.999, 0.3 + (sx + sy) * 0.012 + field[y][x] * 0.002))
            ch = SHADES[int(light * len(SHADES))]
            if color:
                parts.append(f"\x1b[38;5;{BLUES[int(light * len(BLUES))]}m{ch}")
            else:
                parts.append(ch)
        lines.append("".join(parts))
    return "\n".join(lines) + ("\x1b[0m" if color else "")


def main(argv: list[str] | None = None) -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--frames", type=int, default=0)
    ap.add_argument("--width", type=int, default=76)
    ap.add_argument("--height", type=int, default=24)
    ap.add_argument("--fps", type=float, default=24)
    ap.add_argument("--rain", type=float, default=0.12, help="chance of a new drop each frame")
    ap.add_argument("--damping", type=float, default=0.985)
    ap.add_argument("--seed", type=int, default=None)
    ap.add_argument("--no-color", action="store_true")
    a = ap.parse_args(argv)
    rng = random.Random(a.seed)
    w, h = a.width, a.height
    cur = [[0.0] * w for _ in range(h)]
    prev = [[0.0] * w for _ in range(h)]
    drop(cur, w // 2, h // 2, 60, 2)
    frame = drops = 0
    sys.stdout.write("\x1b[?25l\x1b[2J")
    try:
        while not a.frames or frame < a.frames:
            if rng.random() < a.rain:
                drop(cur, rng.randrange(2, w - 2), rng.randrange(2, h - 2), rng.uniform(20, 70), rng.choice((1, 1, 2)))
                drops += 1
            cur, prev = step(cur, prev, a.damping), cur
            sys.stdout.write("\x1b[H" + render(cur, not a.no_color) + f"\nframe {frame}  drops {drops}\x1b[K")
            sys.stdout.flush()
            frame += 1
            time.sleep(1 / a.fps)
    except KeyboardInterrupt:
        pass
    finally:
        sys.stdout.write("\x1b[0m\x1b[?25h\n")


if __name__ == "__main__":
    main()
