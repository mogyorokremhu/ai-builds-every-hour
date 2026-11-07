#!/usr/bin/env python3
"""Conway's Game of Life on a wrapping (toroidal) grid, drawn with half-block characters
so each terminal cell shows two rows of the board.

Usage: python life.py [--frames N] [--pattern random|glider-gun|acorn|rpentomino] [--fps 15]
"""
from __future__ import annotations

import argparse
import random
import sys
import time

PATTERNS: dict[str, list[str]] = {
    "glider-gun": [
        "........................O...........",
        "......................O.O...........",
        "............OO......OO............OO",
        "...........O...O....OO............OO",
        "OO........O.....O...OO..............",
        "OO........O...O.OO....O.O...........",
        "..........O.....O.......O...........",
        "...........O...O....................",
        "............OO......................",
    ],
    "acorn": [".O.....", "...O...", "OO..OOO"],
    "rpentomino": [".OO", "OO.", ".O."],
}


def step(cells: set[tuple[int, int]], w: int, h: int) -> set[tuple[int, int]]:
    """One generation with B3/S23 rules on a w×h torus."""
    counts: dict[tuple[int, int], int] = {}
    for x, y in cells:
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                if dx or dy:
                    k = ((x + dx) % w, (y + dy) % h)
                    counts[k] = counts.get(k, 0) + 1
    return {c for c, n in counts.items() if n == 3 or (n == 2 and c in cells)}


def load(pattern: str, w: int, h: int, rng: random.Random) -> set[tuple[int, int]]:
    if pattern == "random":
        return {(x, y) for y in range(h) for x in range(w) if rng.random() < 0.3}
    rows = PATTERNS[pattern]
    ox = 2 if pattern == "glider-gun" else w // 2 - len(rows[0]) // 2
    oy = 2 if pattern == "glider-gun" else h // 2 - len(rows) // 2
    return {(ox + x, oy + y) for y, row in enumerate(rows) for x, ch in enumerate(row) if ch == "O"}


def render(cells: set[tuple[int, int]], w: int, h: int) -> str:
    lines = []
    for y in range(0, h, 2):
        line = []
        for x in range(w):
            top, bot = (x, y) in cells, (x, y + 1) in cells
            line.append("█" if top and bot else "▀" if top else "▄" if bot else " ")
        lines.append("".join(line))
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--frames", type=int, default=0)
    ap.add_argument("--pattern", default="random", choices=["random", *PATTERNS])
    ap.add_argument("--width", type=int, default=78)
    ap.add_argument("--height", type=int, default=44)
    ap.add_argument("--fps", type=float, default=15)
    ap.add_argument("--seed", type=int, default=None)
    a = ap.parse_args(argv)
    cells = load(a.pattern, a.width, a.height, random.Random(a.seed))
    gen = 0
    sys.stdout.write("\x1b[?25l\x1b[2J")
    try:
        while not a.frames or gen < a.frames:
            sys.stdout.write("\x1b[H" + render(cells, a.width, a.height)
                             + f"\ngeneration {gen:<6} alive {len(cells):<6}")
            sys.stdout.flush()
            cells = step(cells, a.width, a.height)
            gen += 1
            time.sleep(1 / a.fps)
    except KeyboardInterrupt:
        pass
    finally:
        sys.stdout.write("\x1b[?25h\n")


if __name__ == "__main__":
    main()
