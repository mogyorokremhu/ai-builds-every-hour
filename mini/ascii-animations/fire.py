#!/usr/bin/env python3
"""Doom-style ASCII fire: heat rises from the bottom row and cools as it drifts upward.

Usage: python fire.py [--frames N] [--width W] [--height H] [--fps F]
Ctrl+C to stop (the cursor is always restored).
"""
from __future__ import annotations

import argparse
import random
import sys
import time

CHARS = " .:-=+*#%@"
COLORS = [16, 52, 88, 124, 160, 196, 202, 208, 214, 220, 226, 227, 229, 230, 231]


def step(heat: list[list[int]], rng: random.Random, max_heat: int) -> None:
    """Propagate fire one tick: each cell takes heat from below, minus random decay."""
    h, w = len(heat), len(heat[0])
    for x in range(w):
        heat[h - 1][x] = max_heat if rng.random() < 0.85 else max_heat // 2
    for y in range(h - 1):
        for x in range(w):
            src_x = min(w - 1, max(0, x + rng.randint(-1, 1)))
            below = heat[y + 1][src_x]
            heat[y][x] = max(0, below - rng.randint(0, 2))


def render(heat: list[list[int]], max_heat: int, color: bool) -> str:
    rows = []
    for row in heat:
        parts = []
        for v in row:
            ch = CHARS[v * (len(CHARS) - 1) // max_heat]
            if color and v:
                parts.append(f"\x1b[38;5;{COLORS[v * (len(COLORS) - 1) // max_heat]}m{ch}")
            else:
                parts.append(ch)
        rows.append("".join(parts) + ("\x1b[0m" if color else ""))
    return "\n".join(rows)


def main(argv: list[str] | None = None) -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--frames", type=int, default=0, help="stop after N frames (0 = forever)")
    ap.add_argument("--width", type=int, default=70)
    ap.add_argument("--height", type=int, default=22)
    ap.add_argument("--fps", type=float, default=20)
    ap.add_argument("--no-color", action="store_true")
    ap.add_argument("--seed", type=int, default=None)
    a = ap.parse_args(argv)
    rng = random.Random(a.seed)
    max_heat = 36
    heat = [[0] * a.width for _ in range(a.height)]
    frame = 0
    sys.stdout.write("\x1b[?25l\x1b[2J")
    try:
        while not a.frames or frame < a.frames:
            step(heat, rng, max_heat)
            sys.stdout.write("\x1b[H" + render(heat, max_heat, not a.no_color) + "\n")
            sys.stdout.flush()
            frame += 1
            time.sleep(1 / a.fps)
    except KeyboardInterrupt:
        pass
    finally:
        sys.stdout.write("\x1b[0m\x1b[?25h\n")


if __name__ == "__main__":
    main()
