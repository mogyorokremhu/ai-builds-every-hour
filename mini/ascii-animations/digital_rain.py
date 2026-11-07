#!/usr/bin/env python3
"""Falling 'digital rain': columns of glyphs streaming down with bright heads and fading tails.

Usage: python digital_rain.py [--frames N] [--density 0.04] [--fps 20] [--no-color]
"""
from __future__ import annotations

import argparse
import random
import sys
import time

GLYPHS = "ｱｲｳｴｵｶｷｸｹｺｻｼｽｾｿﾀﾁﾂﾃﾄ0123456789ABCDEF:=*+<>"
ASCII_GLYPHS = "0123456789ABCDEF:=*+<>#$%&"


class Drop:
    def __init__(self, x: int, h: int, rng: random.Random) -> None:
        self.x = x
        self.y = -rng.randint(0, h)
        self.speed = rng.choice((1, 1, 2))
        self.length = rng.randint(4, h // 2 + 4)

    def cells(self) -> list[tuple[int, int]]:
        """(y, age) for each visible cell of the drop; age 0 is the bright head."""
        return [(self.y - i, i) for i in range(self.length)]


def render(drops: list[Drop], w: int, h: int, rng: random.Random, glyphs: str, color: bool) -> str:
    grid: list[list[str]] = [[" "] * w for _ in range(h)]
    for d in drops:
        for y, age in d.cells():
            if 0 <= y < h:
                ch = rng.choice(glyphs)
                if color:
                    code = "97" if age == 0 else "92" if age < d.length // 2 else "32"
                    ch = f"\x1b[{code}m{ch}"
                grid[y][d.x] = ch
    return "\n".join("".join(r) for r in grid) + ("\x1b[0m" if color else "")


def main(argv: list[str] | None = None) -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--frames", type=int, default=0)
    ap.add_argument("--width", type=int, default=78)
    ap.add_argument("--height", type=int, default=24)
    ap.add_argument("--density", type=float, default=0.04)
    ap.add_argument("--fps", type=float, default=20)
    ap.add_argument("--ascii", action="store_true", help="avoid wide/katakana glyphs")
    ap.add_argument("--no-color", action="store_true")
    ap.add_argument("--seed", type=int, default=None)
    a = ap.parse_args(argv)
    rng = random.Random(a.seed)
    glyphs = ASCII_GLYPHS if a.ascii else GLYPHS
    drops: list[Drop] = []
    n = 0
    sys.stdout.write("\x1b[?25l\x1b[2J")
    try:
        while not a.frames or n < a.frames:
            for x in range(a.width):
                if rng.random() < a.density and not any(d.x == x and d.y - d.length < 2 for d in drops):
                    drops.append(Drop(x, a.height, rng))
            for d in drops:
                d.y += d.speed
            drops = [d for d in drops if d.y - d.length < a.height]
            sys.stdout.write("\x1b[H" + render(drops, a.width, a.height, rng, glyphs, not a.no_color))
            sys.stdout.flush()
            n += 1
            time.sleep(1 / a.fps)
    except KeyboardInterrupt:
        pass
    finally:
        sys.stdout.write("\x1b[0m\x1b[?25h\n")


if __name__ == "__main__":
    main()
