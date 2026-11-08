#!/usr/bin/env python3
"""Fireworks: rockets rise, explode into particles that fall under gravity and fade (256-colour).

Usage: python fireworks.py [--frames N] [--width 70] [--height 22] [--fps 30] [--seed S] [--no-color]
"""
from __future__ import annotations

import argparse
import math
import random
import sys
import time

PALETTE = [196, 208, 226, 46, 51, 21, 201, 231]


def init(w, h, rng):
    return {"rockets": [], "parts": []}


def step(st, w, h, rng):
    if rng.random() < 0.08:
        st["rockets"].append({"x": rng.uniform(w * 0.2, w * 0.8), "y": h - 1.0, "vy": -rng.uniform(0.7, 1.0), "fuse": rng.randint(10, 18), "c": rng.choice(PALETTE)})
    for r in st["rockets"][:]:
        r["y"] += r["vy"]
        r["fuse"] -= 1
        if r["fuse"] <= 0 or r["y"] < 2:
            st["rockets"].remove(r)
            for _ in range(36):
                ang, sp = rng.uniform(0, 2 * math.pi), rng.uniform(0.2, 1.1)
                st["parts"].append({"x": r["x"], "y": r["y"], "vx": math.cos(ang) * sp * 1.8, "vy": math.sin(ang) * sp * 0.8, "life": rng.randint(14, 26), "max": 26, "c": r["c"]})
    for p in st["parts"][:]:
        p["x"] += p["vx"]
        p["y"] += p["vy"]
        p["vy"] += 0.05
        p["vx"] *= 0.97
        p["life"] -= 1
        if p["life"] <= 0:
            st["parts"].remove(p)


def render(st, w, h, color):
    grid = [[(" ", 0)] * w for _ in range(h)]
    for r in st["rockets"]:
        x, y = int(r["x"]), int(r["y"])
        if 0 <= x < w and 0 <= y < h:
            grid[y][x] = ("|", 231)
    for p in st["parts"]:
        x, y = int(p["x"]), int(p["y"])
        if 0 <= x < w and 0 <= y < h:
            f = p["life"] / p["max"]
            grid[y][x] = ("*" if f > 0.5 else "+" if f > 0.25 else ".", p["c"])
    out = []
    for row in grid:
        out.append("".join(f"\x1b[38;5;{c}m{ch}" if color and ch != " " else ch for ch, c in row) + ("\x1b[0m" if color else ""))
    return "\n".join(out)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--frames", type=int, default=0)
    ap.add_argument("--width", type=int, default=70)
    ap.add_argument("--height", type=int, default=22)
    ap.add_argument("--fps", type=float, default=30)
    ap.add_argument("--seed", type=int, default=None)
    ap.add_argument("--no-color", action="store_true")
    a = ap.parse_args(argv)
    rng = random.Random(a.seed)
    st = init(a.width, a.height, rng)
    n = 0
    try:
        sys.stdout.write("\x1b[2J\x1b[?25l")
        while not a.frames or n < a.frames:
            sys.stdout.write("\x1b[H" + render(st, a.width, a.height, not a.no_color) + "\n")
            sys.stdout.flush()
            step(st, a.width, a.height, rng)
            time.sleep(1 / a.fps)
            n += 1
    except KeyboardInterrupt:
        pass
    finally:
        sys.stdout.write("\x1b[?25h\n")


if __name__ == "__main__":
    main()
