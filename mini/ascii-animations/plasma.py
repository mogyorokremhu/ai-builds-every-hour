#!/usr/bin/env python3
"""Old-school demoscene plasma: a sum of moving sine waves mapped to a colour ramp.

Usage: python plasma.py [--frames N] [--fps 25] [--no-color]
"""
from __future__ import annotations

import argparse
import math
import sys
import time

RAMP = " .:-=+*#%@%#*+=-:. "
PALETTE = [17, 18, 19, 20, 21, 57, 93, 129, 165, 201, 200, 199, 198, 197, 196, 202, 208, 214, 220]


def value(x: float, y: float, t: float) -> float:
    """Plasma field in [0, 1): four interfering waves."""
    v = math.sin(x * 0.16 + t)
    v += math.sin((y * 0.25 + t) * 0.8)
    v += math.sin((x * 0.1 + y * 0.18 + t) * 0.7)
    cx, cy = x * 0.08 + math.sin(t / 3) * 2, y * 0.16 + math.cos(t / 2) * 2
    v += math.sin(math.sqrt(cx * cx + cy * cy + 1) + t)
    return (v + 4) / 8 % 1.0


def render(t: float, w: int, h: int, color: bool) -> str:
    lines = []
    for y in range(h):
        parts = []
        for x in range(w):
            v = value(x, y, t)
            ch = RAMP[int(v * len(RAMP)) % len(RAMP)]
            if color:
                parts.append(f"\x1b[38;5;{PALETTE[int(v * len(PALETTE)) % len(PALETTE)]}m{ch}")
            else:
                parts.append(ch)
        lines.append("".join(parts))
    return "\n".join(lines) + ("\x1b[0m" if color else "")


def main(argv: list[str] | None = None) -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--frames", type=int, default=0)
    ap.add_argument("--width", type=int, default=78)
    ap.add_argument("--height", type=int, default=24)
    ap.add_argument("--fps", type=float, default=25)
    ap.add_argument("--no-color", action="store_true")
    a = ap.parse_args(argv)
    t, n = 0.0, 0
    sys.stdout.write("\x1b[?25l\x1b[2J")
    try:
        while not a.frames or n < a.frames:
            sys.stdout.write("\x1b[H" + render(t, a.width, a.height, not a.no_color))
            sys.stdout.flush()
            t += 0.12
            n += 1
            time.sleep(1 / a.fps)
    except KeyboardInterrupt:
        pass
    finally:
        sys.stdout.write("\x1b[0m\x1b[?25h\n")


if __name__ == "__main__":
    main()
