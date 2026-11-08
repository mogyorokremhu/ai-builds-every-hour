#!/usr/bin/env python3
"""Big digital clock with blinking colon, drawn from a 5x5 block font (24h, local time).

Usage: python clock.py [--frames N] [--fps 4] [--no-color] [--time HH:MM:SS]   (--time freezes the display)
"""
from __future__ import annotations

import argparse
import sys
import time

FONT = {
    "0": ["###", "# #", "# #", "# #", "###"], "1": [" # ", "## ", " # ", " # ", "###"],
    "2": ["###", "  #", "###", "#  ", "###"], "3": ["###", "  #", "###", "  #", "###"],
    "4": ["# #", "# #", "###", "  #", "  #"], "5": ["###", "#  ", "###", "  #", "###"],
    "6": ["###", "#  ", "###", "# #", "###"], "7": ["###", "  #", "  #", "  #", "  #"],
    "8": ["###", "# #", "###", "# #", "###"], "9": ["###", "# #", "###", "  #", "###"],
    ":": ["   ", " # ", "   ", " # ", "   "], " ": ["   "] * 5,
}


def render(text: str, color: bool = True, on: str = "██", off: str = "  ") -> str:
    rows = []
    for r in range(5):
        line = " ".join("".join(on if c == "#" else off for c in FONT[ch][r]) for ch in text)
        rows.append(f"\x1b[38;5;51m{line}\x1b[0m" if color else line)
    return "\n".join(rows)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--frames", type=int, default=0)
    ap.add_argument("--fps", type=float, default=4)
    ap.add_argument("--time", default=None)
    ap.add_argument("--no-color", action="store_true")
    a = ap.parse_args(argv)
    n = 0
    try:
        sys.stdout.write("\x1b[2J\x1b[?25l")
        while not a.frames or n < a.frames:
            t = a.time or time.strftime("%H:%M:%S")
            if n % 2 == 1 and not a.time:
                t = t.replace(":", " ")
            sys.stdout.write("\x1b[H\n" + render(t, not a.no_color) + "\n")
            sys.stdout.flush()
            time.sleep(1 / a.fps)
            n += 1
    except KeyboardInterrupt:
        pass
    finally:
        sys.stdout.write("\x1b[?25h\n")


if __name__ == "__main__":
    main()
