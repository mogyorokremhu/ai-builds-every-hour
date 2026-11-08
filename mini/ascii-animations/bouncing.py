#!/usr/bin/env python3
"""Bouncing balls with gravity, wall bounces and elastic ball–ball collisions, in half-blocks.

Usage: python bouncing.py [--balls N] [--frames N] [--width W] [--height H] [--fps F]
                          [--gravity G] [--restitution E] [--seed S] [--no-color]
Each terminal cell shows two "pixels" (▀ with separate fore/background colours), so the
balls move smoothly at double vertical resolution. Momentum is conserved in collisions.
"""
from __future__ import annotations

import argparse
import math
import random
import sys
import time
from dataclasses import dataclass

PALETTE = [196, 208, 226, 46, 51, 33, 129, 201, 214, 118]


@dataclass
class Ball:
    """A disc in pixel space (y grows downward)."""
    x: float
    y: float
    vx: float
    vy: float
    r: float
    color: int

    @property
    def mass(self) -> float:
        """Mass ∝ area."""
        return self.r * self.r


def collide(a: Ball, b: Ball, restitution: float) -> bool:
    """Resolve an overlap between two balls: separate them and exchange normal momentum."""
    dx, dy = b.x - a.x, b.y - a.y
    dist = math.hypot(dx, dy)
    if dist == 0 or dist >= a.r + b.r:
        return False
    nx, ny = dx / dist, dy / dist
    overlap = a.r + b.r - dist
    ma, mb = a.mass, b.mass
    a.x -= nx * overlap * mb / (ma + mb)
    a.y -= ny * overlap * mb / (ma + mb)
    b.x += nx * overlap * ma / (ma + mb)
    b.y += ny * overlap * ma / (ma + mb)
    rel = (a.vx - b.vx) * nx + (a.vy - b.vy) * ny
    if rel <= 0:
        return True  # already separating
    j = (1 + restitution) * rel / (1 / ma + 1 / mb)
    a.vx -= j / ma * nx
    a.vy -= j / ma * ny
    b.vx += j / mb * nx
    b.vy += j / mb * ny
    return True


def step(balls: list[Ball], w: int, h: int, dt: float, gravity: float, restitution: float) -> int:
    """Advance the simulation by dt; returns the number of ball–ball contacts."""
    for b in balls:
        b.vy += gravity * dt
        b.x += b.vx * dt
        b.y += b.vy * dt
        if b.x - b.r < 0:
            b.x, b.vx = b.r, abs(b.vx) * restitution
        elif b.x + b.r > w:
            b.x, b.vx = w - b.r, -abs(b.vx) * restitution
        if b.y - b.r < 0:
            b.y, b.vy = b.r, abs(b.vy) * restitution
        elif b.y + b.r > h:
            b.y, b.vy = h - b.r, -abs(b.vy) * restitution
            b.vx *= 0.995  # a little floor friction
    hits = 0
    for i in range(len(balls)):
        for k in range(i + 1, len(balls)):
            hits += collide(balls[i], balls[k], restitution)
    return hits


def rasterise(balls: list[Ball], w: int, h: int) -> list[list[int]]:
    """Pixel grid of colour indices (-1 = empty)."""
    px = [[-1] * w for _ in range(h)]
    for b in balls:
        for y in range(max(0, int(b.y - b.r)), min(h, int(b.y + b.r) + 1)):
            for x in range(max(0, int(b.x - b.r)), min(w, int(b.x + b.r) + 1)):
                if (x + 0.5 - b.x) ** 2 + (y + 0.5 - b.y) ** 2 <= b.r * b.r:
                    px[y][x] = b.color
    return px


def render(px: list[list[int]], color: bool) -> str:
    """Two pixel rows per text row using the upper-half block."""
    lines = []
    for y in range(0, len(px) - 1, 2):
        parts = []
        for top, bot in zip(px[y], px[y + 1]):
            if not color:
                parts.append("█" if top >= 0 and bot >= 0 else "▀" if top >= 0 else "▄" if bot >= 0 else " ")
                continue
            fg = f"38;5;{top}" if top >= 0 else "38;5;234"
            bg = f"48;5;{bot}" if bot >= 0 else "48;5;234"
            parts.append(f"\x1b[{fg};{bg}m▀")
        lines.append("".join(parts) + ("\x1b[0m" if color else ""))
    return "\n".join(lines)


def kinetic(balls: list[Ball]) -> float:
    """Total kinetic energy."""
    return sum(0.5 * b.mass * (b.vx * b.vx + b.vy * b.vy) for b in balls)


def main(argv: list[str] | None = None) -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--balls", type=int, default=9)
    ap.add_argument("--frames", type=int, default=0)
    ap.add_argument("--width", type=int, default=76)
    ap.add_argument("--height", type=int, default=22, help="text rows (pixels = 2×)")
    ap.add_argument("--fps", type=float, default=30)
    ap.add_argument("--gravity", type=float, default=60.0, help="pixels / s²")
    ap.add_argument("--restitution", type=float, default=0.92)
    ap.add_argument("--seed", type=int, default=None)
    ap.add_argument("--no-color", action="store_true")
    a = ap.parse_args(argv)
    rng = random.Random(a.seed)
    w, h = a.width, a.height * 2
    balls: list[Ball] = []
    while len(balls) < a.balls:
        r = rng.uniform(2.0, 4.5)
        b = Ball(rng.uniform(r, w - r), rng.uniform(r, h / 2), rng.uniform(-30, 30), rng.uniform(-10, 10), r,
                 PALETTE[len(balls) % len(PALETTE)])
        if all(math.hypot(b.x - o.x, b.y - o.y) > b.r + o.r for o in balls) or len(balls) > a.balls * 20:
            balls.append(b)
    frame = hits = 0
    sys.stdout.write("\x1b[?25l\x1b[2J")
    try:
        while not a.frames or frame < a.frames:
            for _ in range(4):
                hits += step(balls, w, h, 1 / 120, a.gravity, a.restitution)  # 1/30 s of physics per frame
            if all(abs(b.vy) < 3 and b.y + b.r >= h - 0.5 for b in balls):
                for b in balls:  # everything has settled: kick them back up
                    b.vy = -rng.uniform(40, 80)
                    b.vx += rng.uniform(-25, 25)
            sys.stdout.write("\x1b[H" + render(rasterise(balls, w, h), not a.no_color)
                             + f"\nframe {frame}  balls {len(balls)}  contacts {hits}  energy {kinetic(balls):8.0f}\x1b[K")
            sys.stdout.flush()
            frame += 1
            time.sleep(1 / a.fps)
    except KeyboardInterrupt:
        pass
    finally:
        sys.stdout.write("\x1b[0m\x1b[?25h\n")


if __name__ == "__main__":
    main()
