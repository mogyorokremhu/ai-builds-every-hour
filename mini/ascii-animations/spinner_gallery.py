#!/usr/bin/env python3
"""Spinner gallery: a dozen classic terminal spinners side by side.

Usage: python spinner_gallery.py [--fps 12] [--frames N]
"""
import argparse
import sys
import time

SPINNERS = {
    "line": "|/-\\",
    "dots": "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏",
    "arc": "◜◠◝◞◡◟",
    "bar": "▁▂▃▄▅▆▇█▇▆▅▄▃▂",
    "grow": "▉▊▋▌▍▎▏▎▍▌▋▊▉",
    "arrows": "←↖↑↗→↘↓↙",
    "box": "▖▘▝▗",
    "pulse": "·•●•",
    "moon": "○◔◑◕●◕◑◔",
    "bounce": "⠁⠂⠄⡀⢀⠠⠐⠈",
    "toggle": "⊶⊷",
    "star": "✶✸✹✺✹✸",
}


def frame(i):
    return "\n".join(f"{name:>8}  {s[i % len(s)]}" for name, s in SPINNERS.items())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fps", type=float, default=12)
    ap.add_argument("--frames", type=int, default=0)
    a = ap.parse_args()
    i = 0
    while a.frames == 0 or i < a.frames:
        sys.stdout.write("\x1b[H\x1b[2J" + frame(i) + "\n")
        sys.stdout.flush()
        time.sleep(1 / a.fps)
        i += 1


if __name__ == "__main__":
    main()
