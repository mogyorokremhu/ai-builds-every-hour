#!/usr/bin/env python3
"""Big-digit countdown timer drawn with 3x5 block glyphs.

Usage: python countdown.py [--from 10] [--frames N] [--fps 2]
"""
import argparse
import sys
import time

GLYPHS = {
    "0": ["###", "# #", "# #", "# #", "###"],
    "1": [" # ", "## ", " # ", " # ", "###"],
    "2": ["###", "  #", "###", "#  ", "###"],
    "3": ["###", "  #", "###", "  #", "###"],
    "4": ["# #", "# #", "###", "  #", "  #"],
    "5": ["###", "#  ", "###", "  #", "###"],
    "6": ["###", "#  ", "###", "# #", "###"],
    "7": ["###", "  #", "  #", "  #", "  #"],
    "8": ["###", "# #", "###", "# #", "###"],
    "9": ["###", "# #", "###", "  #", "###"],
}


def big(n):
    text = str(n)
    return "\n".join("  ".join(GLYPHS[c][r] for c in text) for r in range(5))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--from", dest="start", type=int, default=10)
    ap.add_argument("--frames", type=int, default=0)
    ap.add_argument("--fps", type=float, default=2)
    a = ap.parse_args()
    n, shown = a.start, 0
    try:
        while n >= 0 and (a.frames == 0 or shown < a.frames):
            sys.stdout.write("\x1b[H\x1b[2J" + big(n) + "\n")
            sys.stdout.flush()
            time.sleep(1 / a.fps)
            n -= 1
            shown += 1
        if n < 0:
            print("\nLIFTOFF!")
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
