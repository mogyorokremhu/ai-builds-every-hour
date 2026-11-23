#!/usr/bin/env python3
"""Fireflies: blinking lights drifting over a dark meadow.

Usage: python fireflies.py [--frames N] [--fps 12] [--seed S] [--count 14]
"""
import argparse
import math
import random
import sys
import time

W, H = 50, 16


def make(count, rng):
    return [{"x": rng.uniform(0, W), "y": rng.uniform(0, H - 2),
             "a": rng.uniform(0, 6.28), "ph": rng.uniform(0, 6.28),
             "rate": rng.uniform(0.15, 0.4)} for _ in range(count)]


def step(flies, t, rng):
    """Move fireflies; return brightness 0..1 for each."""
    out = []
    for f in flies:
        f["a"] += rng.uniform(-0.4, 0.4)
        f["x"] = (f["x"] + math.cos(f["a"]) * 0.5) % W
        f["y"] = min(H - 2, max(0, f["y"] + math.sin(f["a"]) * 0.3))
        out.append(max(0.0, math.sin(t * f["rate"] + f["ph"])) ** 3)
    return out


def render(flies, bright):
    grid = [[" "] * W for _ in range(H)]
    grid[H - 1] = ["\"" if (x * 7) % 3 else "'" for x in range(W)]
    for f, b in zip(flies, bright):
        if b > 0.05:
            grid[int(f["y"])][int(f["x"])] = "@*+."[min(3, int((1 - b) * 4))]
    return "\n".join("".join(r) for r in grid)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--frames", type=int, default=120)
    p.add_argument("--fps", type=float, default=12)
    p.add_argument("--seed", type=int, default=None)
    p.add_argument("--count", type=int, default=14)
    a = p.parse_args()
    rng = random.Random(a.seed)
    flies = make(a.count, rng)
    for t in range(a.frames):
        sys.stdout.write("\x1b[H\x1b[2J" + render(flies, step(flies, t, rng)) + "\n")
        sys.stdout.flush()
        time.sleep(1 / a.fps)


if __name__ == "__main__":
    main()
