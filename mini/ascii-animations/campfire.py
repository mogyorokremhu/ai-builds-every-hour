#!/usr/bin/env python3
"""Campfire: rising sparks and flickering flames over a log pile.

Usage: python campfire.py [--frames N] [--fps 15] [--seed S]
"""
import argparse
import random
import sys
import time

W, H = 30, 14
FLAME = " .:^*#"


def step(heat, sparks, rng):
    """Advance flame heat grid (row 0 = top) and spark list one frame."""
    for x in range(W):
        heat[H - 1][x] = rng.random() * (1.0 - abs(x - W / 2) / (W / 2) * 0.9)
    for y in range(H - 1):
        for x in range(W):
            below = [heat[y + 1][max(0, x - 1)], heat[y + 1][x], heat[y + 1][min(W - 1, x + 1)]]
            heat[y][x] = max(0.0, sum(below) / 3 * 0.86 - rng.random() * 0.04)
    if rng.random() < 0.4:
        sparks.append([W / 2 + rng.uniform(-4, 4), H - 3.0])
    out = []
    for sx, sy in sparks:
        sy -= 0.5 + rng.random() * 0.4
        sx += rng.uniform(-0.6, 0.6)
        if sy > 0 and 0 <= sx < W:
            out.append([sx, sy])
    sparks[:] = out


def render(heat, sparks):
    rows = [[FLAME[min(len(FLAME) - 1, int(c * len(FLAME) * 1.3))] for c in row] for row in heat]
    for sx, sy in sparks:
        rows[int(sy)][int(sx)] = "'"
    lines = ["".join(r) for r in rows]
    lines.append("=" * W)
    lines.append("  \\\\\\\\ (logs) ////".center(W))
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--frames", type=int, default=0)
    ap.add_argument("--fps", type=float, default=15)
    ap.add_argument("--seed", type=int, default=None)
    a = ap.parse_args()
    rng = random.Random(a.seed)
    heat = [[0.0] * W for _ in range(H)]
    sparks = []
    f = 0
    while a.frames == 0 or f < a.frames:
        step(heat, sparks, rng)
        sys.stdout.write("\x1b[H\x1b[2J" + render(heat, sparks) + "\n")
        sys.stdout.flush()
        time.sleep(1 / a.fps)
        f += 1


if __name__ == "__main__":
    main()
