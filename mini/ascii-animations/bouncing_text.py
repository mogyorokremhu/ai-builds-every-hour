#!/usr/bin/env python3
"""A text banner bounces around the screen like a DVD logo and counts corner hits.

Usage: python bouncing_text.py [--text HELLO] [--frames N] [--width 50] [--height 14] [--fps 15]
"""
import argparse
import sys
import time


def move(x, y, dx, dy, tw, w, h):
    """Advance one cell, bouncing off walls. Returns x, y, dx, dy, corner_hit."""
    x, y = x + dx, y + dy
    hit_x = hit_y = False
    if x < 0 or x + tw > w:
        dx, hit_x = -dx, True
        x = max(0, min(x, w - tw))
    if y < 0 or y >= h:
        dy, hit_y = -dy, True
        y = max(0, min(y, h - 1))
    return x, y, dx, dy, hit_x and hit_y


def render(text, x, y, w, h, corners):
    rows = [[" "] * w for _ in range(h)]
    for i, c in enumerate(text):
        rows[y][x + i] = c
    body = ["|" + "".join(r) + "|" for r in rows]
    edge = "+" + "-" * w + "+"
    return "\n".join([edge] + body + [edge, f"corner hits: {corners}"])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--text", default="HELLO")
    ap.add_argument("--frames", type=int, default=0)
    ap.add_argument("--width", type=int, default=50)
    ap.add_argument("--height", type=int, default=14)
    ap.add_argument("--fps", type=float, default=15)
    a = ap.parse_args()
    x, y, dx, dy, corners, n = 0, 0, 1, 1, 0, 0
    while a.frames == 0 or n < a.frames:
        x, y, dx, dy, hit = move(x, y, dx, dy, len(a.text), a.width, a.height)
        corners += hit
        sys.stdout.write("\x1b[H" + render(a.text, x, y, a.width, a.height, corners) + "\n")
        sys.stdout.flush()
        n += 1
        time.sleep(1 / a.fps)


if __name__ == "__main__":
    main()
