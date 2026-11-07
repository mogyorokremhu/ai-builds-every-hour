#!/usr/bin/env python3
"""3D starfield: stars fly towards the viewer with perspective projection.

Usage: python starfield.py [--frames N] [--stars 200] [--fps 30]
"""
from __future__ import annotations

import argparse
import random
import sys
import time

GLYPHS = "@*+·."  # near -> far


def new_star(rng: random.Random, far: bool = True) -> list[float]:
    return [rng.uniform(-1, 1), rng.uniform(-1, 1), rng.uniform(0.6, 1.0) if far else rng.uniform(0.05, 1.0)]


def project(star: list[float], w: int, h: int) -> tuple[int, int] | None:
    """Perspective-project a star at (x, y, z) to screen coordinates (None if off screen)."""
    x, y, z = star
    if z <= 0.01:
        return None
    sx = int(w / 2 + x / z * w / 2)
    sy = int(h / 2 + y / z * h / 2)
    if 0 <= sx < w and 0 <= sy < h:
        return sx, sy
    return None


def frame(stars: list[list[float]], w: int, h: int, speed: float, rng: random.Random) -> str:
    grid = [[" "] * w for _ in range(h)]
    for i, s in enumerate(stars):
        s[2] -= speed
        p = project(s, w, h)
        if p is None:
            stars[i] = new_star(rng)
            continue
        idx = min(len(GLYPHS) - 1, int(s[2] * len(GLYPHS)))
        grid[p[1]][p[0]] = GLYPHS[idx]
    return "\n".join("".join(r) for r in grid)


def main(argv: list[str] | None = None) -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--frames", type=int, default=0)
    ap.add_argument("--stars", type=int, default=200)
    ap.add_argument("--width", type=int, default=78)
    ap.add_argument("--height", type=int, default=24)
    ap.add_argument("--speed", type=float, default=0.02)
    ap.add_argument("--fps", type=float, default=30)
    ap.add_argument("--seed", type=int, default=None)
    a = ap.parse_args(argv)
    rng = random.Random(a.seed)
    stars = [new_star(rng, far=False) for _ in range(a.stars)]
    n = 0
    sys.stdout.write("\x1b[?25l\x1b[2J")
    try:
        while not a.frames or n < a.frames:
            sys.stdout.write("\x1b[H" + frame(stars, a.width, a.height, a.speed, rng))
            sys.stdout.flush()
            n += 1
            time.sleep(1 / a.fps)
    except KeyboardInterrupt:
        pass
    finally:
        sys.stdout.write("\x1b[?25h\n")


if __name__ == "__main__":
    main()
