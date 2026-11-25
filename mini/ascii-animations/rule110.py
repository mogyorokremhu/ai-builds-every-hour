#!/usr/bin/env python3
"""Elementary cellular automaton (default Rule 110) scrolling down the terminal.

Usage: python rule110.py [--rule N] [--frames N] [--width W] [--height H] [--fps F] [--seed S]
Each new row is computed from the previous one; the picture scrolls upward.
"""
from __future__ import annotations

import argparse
import random
import time


def next_row(row: list[int], rule: int) -> list[int]:
    """Apply an elementary CA rule (0-255) to a row with wrap-around edges."""
    n = len(row)
    return [(rule >> (row[(i - 1) % n] * 4 + row[i] * 2 + row[(i + 1) % n])) & 1 for i in range(n)]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--rule", type=int, default=110)
    ap.add_argument("--frames", type=int, default=0)
    ap.add_argument("--width", type=int, default=72)
    ap.add_argument("--height", type=int, default=24)
    ap.add_argument("--fps", type=float, default=15)
    ap.add_argument("--seed", type=int, default=None)
    a = ap.parse_args()
    rng = random.Random(a.seed)
    row = [rng.randint(0, 1) for _ in range(a.width)]
    rows = [row]
    frame = 0
    try:
        while a.frames == 0 or frame < a.frames:
            row = next_row(row, a.rule)
            rows = (rows + [row])[-a.height:]
            print("\x1b[H" + "\n".join("".join("█" if c else " " for c in r) for r in rows)
                  + f"\nrule {a.rule}", flush=True)
            frame += 1
            time.sleep(1 / a.fps)
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
