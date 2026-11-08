#!/usr/bin/env python3
"""A rotating colour spiral tunnel: pixels shaded by angle + log-radius, scrolling inward (256-colour).

Usage: python spiral.py [--frames N] [--arms 4] [--width 70] [--height 22] [--fps 30] [--no-color]
"""
from __future__ import annotations

import argparse
import math
import sys
import time

SHADES = " .:-=+*#%@"


def value(x: float, y: float, t: float, arms: int) -> float:
    """Brightness 0..1 at normalised coords (aspect-corrected)."""
    r = math.hypot(x, y) or 1e-6
    ang = math.atan2(y, x)
    return 0.5 + 0.5 * math.sin(arms * ang + 6 * math.log(r) - t)


def render(w: int, h: int, t: float, arms: int, color: bool) -> str:
    rows = []
    for j in range(h):
        row = []
        for i in range(w):
            x, y = (i / w - 0.5) * 2 * (w / h) / 2, (j / h - 0.5) * 2
            v = value(x, y, t, arms)
            ch = SHADES[min(len(SHADES) - 1, int(v * len(SHADES)))]
            row.append(f"\x1b[38;5;{16 + int(v * 35)}m{ch}" if color else ch)
        rows.append("".join(row) + ("\x1b[0m" if color else ""))
    return "\n".join(rows)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--frames", type=int, default=0)
    ap.add_argument("--arms", type=int, default=4)
    ap.add_argument("--width", type=int, default=70)
    ap.add_argument("--height", type=int, default=22)
    ap.add_argument("--fps", type=float, default=30)
    ap.add_argument("--no-color", action="store_true")
    a = ap.parse_args(argv)
    n = 0
    try:
        sys.stdout.write("\x1b[2J\x1b[?25l")
        while not a.frames or n < a.frames:
            sys.stdout.write("\x1b[H" + render(a.width, a.height, n * 0.15, a.arms, not a.no_color) + "\n")
            sys.stdout.flush()
            time.sleep(1 / a.fps)
            n += 1
    except KeyboardInterrupt:
        pass
    finally:
        sys.stdout.write("\x1b[?25h\n")


if __name__ == "__main__":
    main()
