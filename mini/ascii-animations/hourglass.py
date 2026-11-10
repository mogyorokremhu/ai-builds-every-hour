#!/usr/bin/env python3
"""Hourglass: sand grains fall through the neck and pile up below.

Usage: python hourglass.py [--grains 60] [--fps 25] [--frames N]
"""
import argparse
import sys
import time

# Per row: inclusive x range inside the glass; everything else is wall.
ROWS = [(0, 10), (1, 9), (2, 8), (3, 7), (4, 6), (5, 5),
        (5, 5), (4, 6), (3, 7), (2, 8), (1, 9), (0, 10)]
NECK = 5


def inside(x, y):
    if not 0 <= y < len(ROWS):
        return False
    a, b = ROWS[y]
    return a <= x <= b


def step(sand):
    """Move each grain down, or diagonally if blocked; bottom-up order."""
    moved = False
    occ = set(sand)
    new = []
    for (x, y) in sorted(sand, key=lambda p: -p[1]):
        occ.discard((x, y))
        for dx in (0, -1, 1):
            nx, ny = x + dx, y + 1
            if inside(nx, ny) and (nx, ny) not in occ:
                x, y, moved = nx, ny, True
                break
        occ.add((x, y))
        new.append((x, y))
    return new, moved


def render(sand):
    s = set(sand)
    lines = ["+" + "-" * 11 + "+"]
    for y, (a, b) in enumerate(ROWS):
        row = "".join(("o" if (x, y) in s else " ") if a <= x <= b else "#" for x in range(11))
        lines.append("|" + row + "|")
    lines.append("+" + "-" * 11 + "+")
    return "\n".join(lines)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--grains", type=int, default=30)
    p.add_argument("--fps", type=float, default=25)
    p.add_argument("--frames", type=int, default=200)
    a = p.parse_args()
    sand = [(x, y) for y in range(NECK) for x in range(ROWS[y][0], ROWS[y][1] + 1)][: a.grains]
    for _ in range(a.frames):
        sys.stdout.write("\x1b[H\x1b[2J" + render(sand) + "\n")
        sys.stdout.flush()
        sand, moved = step(sand)
        time.sleep(1 / a.fps)
        if not moved:
            break


if __name__ == "__main__":
    main()
