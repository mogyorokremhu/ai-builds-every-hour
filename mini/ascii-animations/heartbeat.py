#!/usr/bin/env python3
"""ECG heartbeat monitor: a scrolling trace with a P-QRS-T wave every beat.

Usage: python heartbeat.py [--frames N] [--width 60] [--height 11] [--bpm 70] [--fps 20]
"""
import argparse
import sys
import time

# one beat as relative amplitudes in -1..1 (flat, P bump, Q dip, R spike, S dip, T bump, flat)
BEAT = [0, 0, .15, .2, .15, 0, 0, -.2, 1.0, -.45, 0, 0, 0, .25, .35, .25, 0, 0]


def signal(t, period):
    i = t % period
    return BEAT[i] if i < len(BEAT) else 0.0


def render(trace, height):
    mid = height // 2
    grid = [[" "] * len(trace) for _ in range(height)]
    for x, v in enumerate(trace):
        y = mid - round(v * mid)
        grid[max(0, min(height - 1, y))][x] = "*"
    return "\n".join("".join(r) for r in grid)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--frames", type=int, default=0)
    ap.add_argument("--width", type=int, default=60)
    ap.add_argument("--height", type=int, default=11)
    ap.add_argument("--bpm", type=int, default=70)
    ap.add_argument("--fps", type=float, default=20)
    a = ap.parse_args()
    period = max(len(BEAT), int(60 * a.fps / a.bpm))
    trace, n = [0.0] * a.width, 0
    try:
        while a.frames == 0 or n < a.frames:
            trace = trace[1:] + [signal(n, period)]
            sys.stdout.write("\x1b[H\x1b[2J" + render(trace, a.height) + f"\n{a.bpm} bpm\n")
            sys.stdout.flush()
            n += 1
            time.sleep(1 / a.fps)
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
