#!/usr/bin/env python3
"""A spinning, shaded 3D torus rendered with a z-buffer and luminance characters.

For every (theta, phi) on the torus surface we rotate the point around two axes,
project it, keep the nearest point per screen cell, and pick a character from the
dot product of the surface normal with a light direction.

Usage: python torus.py [--frames N] [--fps 30]
"""
from __future__ import annotations

import argparse
import math
import sys
import time

SHADES = ".,-~:;=!*#$@"


def render(a: float, b: float, w: int = 78, h: int = 24, r1: float = 1.0, r2: float = 2.0,
           dist: float = 5.0) -> str:
    """Render the torus rotated by angles ``a`` (around X) and ``b`` (around Z)."""
    k1 = w * dist * 3 / (8 * (r1 + r2))
    out = [" "] * (w * h)
    zbuf = [0.0] * (w * h)
    ca, sa, cb, sb = math.cos(a), math.sin(a), math.cos(b), math.sin(b)
    theta = 0.0
    while theta < 2 * math.pi:
        ct, st = math.cos(theta), math.sin(theta)
        phi = 0.0
        while phi < 2 * math.pi:
            cp, sp = math.cos(phi), math.sin(phi)
            cx, cy = r2 + r1 * ct, r1 * st          # circle before revolving
            x = cx * (cb * cp + sa * sb * sp) - cy * ca * sb
            y = cx * (sb * cp - sa * cb * sp) + cy * ca * cb
            z = dist + ca * cx * sp + cy * sa
            ooz = 1 / z
            xp = int(w / 2 + k1 * ooz * x)
            yp = int(h / 2 - k1 * ooz * y * 0.5)
            lum = cp * ct * sb - ca * ct * sp - sa * st + cb * (ca * st - ct * sa * sp)
            if 0 <= xp < w and 0 <= yp < h and lum > 0:
                i = xp + yp * w
                if ooz > zbuf[i]:
                    zbuf[i] = ooz
                    out[i] = SHADES[min(len(SHADES) - 1, int(lum * 8))]
            phi += 0.012
        theta += 0.035
    return "\n".join("".join(out[r * w:(r + 1) * w]) for r in range(h))


def main(argv: list[str] | None = None) -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--frames", type=int, default=0)
    ap.add_argument("--fps", type=float, default=30)
    a = ap.parse_args(argv)
    ang_a = ang_b = 0.0
    n = 0
    sys.stdout.write("\x1b[?25l\x1b[2J")
    try:
        while not a.frames or n < a.frames:
            sys.stdout.write("\x1b[H" + render(ang_a, ang_b))
            sys.stdout.flush()
            ang_a += 0.07
            ang_b += 0.03
            n += 1
            time.sleep(1 / a.fps)
    except KeyboardInterrupt:
        pass
    finally:
        sys.stdout.write("\x1b[?25h\n")


if __name__ == "__main__":
    main()
