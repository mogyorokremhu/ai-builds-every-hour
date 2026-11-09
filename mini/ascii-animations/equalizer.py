#!/usr/bin/env python3
"""Audio-style equalizer: bars bounce toward random targets and fall with gravity.

Usage: python equalizer.py [--frames N] [--bars 16] [--height 10] [--fps 15] [--seed S]
"""
import argparse
import random
import sys
import time


def step(levels, targets, rng, height):
    """Advance one frame: rise quickly toward the target, then decay."""
    for i in range(len(levels)):
        if rng.random() < 0.25:
            targets[i] = rng.uniform(1, height)
        if levels[i] < targets[i]:
            levels[i] = min(targets[i], levels[i] + 2.5)
        else:
            levels[i] = max(0.0, levels[i] - 0.7)
        if levels[i] >= targets[i]:
            targets[i] = max(0.0, targets[i] - 0.5)


def render(levels, height):
    rows = []
    for y in range(height, 0, -1):
        rows.append(" ".join("##" if round(l) >= y else "  " for l in levels))
    rows.append("-- " * (len(levels) * 2 // 3))
    return "\n".join(rows)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--frames", type=int, default=0)
    ap.add_argument("--bars", type=int, default=16)
    ap.add_argument("--height", type=int, default=10)
    ap.add_argument("--fps", type=float, default=15)
    ap.add_argument("--seed", type=int, default=None)
    a = ap.parse_args()
    rng = random.Random(a.seed)
    levels, targets = [0.0] * a.bars, [0.0] * a.bars
    n = 0
    while a.frames == 0 or n < a.frames:
        step(levels, targets, rng, a.height)
        sys.stdout.write("\x1b[H\x1b[J" + render(levels, a.height) + "\n")
        sys.stdout.flush()
        n += 1
        time.sleep(1 / a.fps)


if __name__ == "__main__":
    main()
