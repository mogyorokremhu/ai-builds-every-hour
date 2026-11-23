#!/usr/bin/env python3
"""Conveyor: boxes riding a belt, with a sorting gate that bumps big ones up.

Usage: python conveyor.py [--frames N] [--fps 10] [--seed S]
"""
import argparse
import random
import sys
import time

W = 48


def step(boxes, t, rng):
    """Advance boxes one cell; spawn new ones; drop those past the end."""
    boxes = [(x + 1, s) for x, s in boxes if x + 1 < W]
    if t % 5 == 0:
        boxes.append((0, rng.choice("sS")))
    return boxes


def render(boxes, t):
    top = [" "] * W
    mid = [" "] * W
    for x, s in boxes:
        mid[x] = "#" if s == "S" else "o"
        if s == "S" and 20 <= x <= 28:
            top[x], mid[x] = "#", " "  # big boxes hop over the gate
    belt = "".join("=" if (i + t) % 4 else "-" for i in range(W))
    gate = " " * 20 + "|_____|".ljust(W - 20)
    wheels = "(O)" + " " * (W - 6) + "(O)"
    return "\n".join(["".join(top), gate, "".join(mid), belt, wheels])


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--frames", type=int, default=100)
    p.add_argument("--fps", type=float, default=10)
    p.add_argument("--seed", type=int, default=None)
    a = p.parse_args()
    rng = random.Random(a.seed)
    boxes = []
    for t in range(a.frames):
        boxes = step(boxes, t, rng)
        sys.stdout.write("\x1b[H\x1b[2J" + render(boxes, t) + "\n")
        sys.stdout.flush()
        time.sleep(1 / a.fps)


if __name__ == "__main__":
    main()
