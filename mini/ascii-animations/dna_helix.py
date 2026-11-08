#!/usr/bin/env python3
"""A rotating DNA double helix scrolling down the screen, with paired bases A–T and C–G.

Usage: python dna_helix.py [--frames N] [--height H] [--width W] [--fps F] [--sequence ACGT...]
                           [--seed S] [--no-color]
The two backbones are 3D sines seen side-on: depth decides which strand is drawn in front
(bold) and which behind (dim), and rungs are drawn between them with the base letters.
"""
from __future__ import annotations

import argparse
import math
import random
import sys
import time

PAIR = {"A": "T", "T": "A", "C": "G", "G": "C"}
BASE_COLOR = {"A": 203, "T": 220, "C": 81, "G": 120}
TWIST = 0.42          # radians of rotation per row (≈ 10.5 base pairs per turn, like B-DNA)


def strand_x(phase: float, center: int, radius: float) -> tuple[float, float, float, float]:
    """Screen x and depth of both backbones at rotation `phase` (depth > 0 = towards you)."""
    return (center + radius * math.sin(phase), math.cos(phase),
            center + radius * math.sin(phase + math.pi), math.cos(phase + math.pi))


def row_cells(base: str, phase: float, width: int, radius: float) -> list[tuple[int, str, str]]:
    """The characters of one helix row as (column, char, style) where style is front/back/rung/base."""
    c = width // 2
    x1, z1, x2, z2 = strand_x(phase, c, radius)
    a, b = round(x1), round(x2)
    cells: list[tuple[int, str, str]] = []
    lo, hi = sorted((a, b))
    if hi - lo >= 4:  # rung with letters near each strand
        left_base, right_base = (base, PAIR[base]) if a < b else (PAIR[base], base)
        for x in range(lo + 1, hi):
            cells.append((x, "-", "rung"))
        cells.append((lo + 1, left_base, "base"))
        cells.append((hi - 1, right_base, "base"))
    for z, x in sorted([(z1, a), (z2, b)]):  # back strand first, the front one overwrites it
        cells.append((x, "O" if z > 0.35 else "o" if z > -0.35 else ".", "front" if z >= 0 else "back"))
    return cells


def render_row(cells: list[tuple[int, str, str]], width: int, color: bool) -> str:
    """Compose a row; later cells overwrite earlier ones."""
    chars = [" "] * width
    styles = [""] * width
    for x, ch, style in cells:
        if 0 <= x < width:
            chars[x] = ch
            styles[x] = style
    if not color:
        return "".join(chars)
    out = []
    for ch, st in zip(chars, styles):
        if st == "front":
            out.append(f"\x1b[1;38;5;231m{ch}\x1b[0m")
        elif st == "back":
            out.append(f"\x1b[38;5;240m{ch}\x1b[0m")
        elif st == "rung":
            out.append(f"\x1b[38;5;244m{ch}\x1b[0m")
        elif st == "base":
            out.append(f"\x1b[1;38;5;{BASE_COLOR[ch]}m{ch}\x1b[0m")
        else:
            out.append(ch)
    return "".join(out)


def main(argv: list[str] | None = None) -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--frames", type=int, default=0)
    ap.add_argument("--height", type=int, default=24)
    ap.add_argument("--width", type=int, default=40)
    ap.add_argument("--fps", type=float, default=12)
    ap.add_argument("--sequence", default="", help="bases to scroll (random if empty)")
    ap.add_argument("--seed", type=int, default=None)
    ap.add_argument("--no-color", action="store_true")
    a = ap.parse_args(argv)
    rng = random.Random(a.seed)
    seq = [b for b in a.sequence.upper() if b in PAIR]
    radius = a.width / 2 - 3
    strand: list[str] = []
    frame = 0
    sys.stdout.write("\x1b[?25l\x1b[2J")
    try:
        while not a.frames or frame < a.frames:
            while len(strand) < frame + a.height:
                strand.append(seq[len(strand) % len(seq)] if seq else rng.choice("ACGT"))
            lines = []
            for row in range(a.height):
                i = frame + row
                phase = i * TWIST + frame * 0.15
                lines.append(render_row(row_cells(strand[i], phase, a.width, radius), a.width, not a.no_color))
            gc = sum(b in "GC" for b in strand[frame:frame + a.height]) / a.height
            sys.stdout.write("\x1b[H" + "\n".join(lines) + f"\nbase pair {frame}  GC content (on screen) {gc:.0%}\x1b[K")
            sys.stdout.flush()
            frame += 1
            time.sleep(1 / a.fps)
    except KeyboardInterrupt:
        pass
    finally:
        sys.stdout.write("\x1b[0m\x1b[?25h\n")


if __name__ == "__main__":
    main()
