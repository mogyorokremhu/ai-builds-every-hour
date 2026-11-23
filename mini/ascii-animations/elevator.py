#!/usr/bin/env python3
"""Elevator: a car serving random floor requests with SCAN-style direction.

Usage: python elevator.py [--frames N] [--fps 6] [--seed S] [--floors 8]
"""
import argparse
import random
import sys
import time


def next_dir(pos, d, reqs):
    """Keep going while requests lie ahead, else reverse, else idle (0)."""
    if any((r - pos) * d > 0 for r in reqs):
        return d
    if any((r - pos) * -d > 0 for r in reqs):
        return -d
    return 0


def step(pos, d, reqs):
    """One tick: serve the current floor, then move. Returns (pos, dir)."""
    reqs.discard(pos)
    d = next_dir(pos, d or 1, reqs) if reqs else 0
    return pos + d, d


def render(pos, d, reqs, floors):
    rows = []
    for f in range(floors - 1, -1, -1):
        car = "[^]" if (f == pos and d > 0) else "[v]" if (f == pos and d < 0) else "[ ]" if f == pos else "   "
        call = " *" if f in reqs else "  "
        rows.append(f"{f:>2} |{car}|{call}")
    return "\n".join(rows)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--frames", type=int, default=80)
    p.add_argument("--fps", type=float, default=6)
    p.add_argument("--seed", type=int, default=None)
    p.add_argument("--floors", type=int, default=8)
    a = p.parse_args()
    rng = random.Random(a.seed)
    pos, d, reqs = 0, 0, set()
    for _ in range(a.frames):
        if rng.random() < 0.25:
            reqs.add(rng.randrange(a.floors))
        pos, d = step(pos, d, reqs)
        pos = max(0, min(a.floors - 1, pos))
        sys.stdout.write("\x1b[H\x1b[2J" + render(pos, d, reqs, a.floors) + "\n")
        sys.stdout.flush()
        time.sleep(1 / a.fps)


if __name__ == "__main__":
    main()
