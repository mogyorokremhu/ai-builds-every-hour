#!/usr/bin/env python3
"""Chaotic double pendulum: RK4-integrated equations of motion with a fading trail.

Usage: python double_pendulum.py [--frames N] [--width W] [--height H] [--fps F]
                                 [--theta1 DEG] [--theta2 DEG] [--no-color]
Two pendulums started 0.01° apart are drawn together (--twin) to show sensitive dependence.
"""
from __future__ import annotations

import argparse
import math
import sys
import time

G, L1, L2, M1, M2 = 9.81, 1.0, 1.0, 1.0, 1.0
TRAIL = ".:-=+*#"


def derivs(s: tuple[float, float, float, float]) -> tuple[float, float, float, float]:
    """Time derivatives of (θ1, ω1, θ2, ω2) for the frictionless double pendulum."""
    t1, w1, t2, w2 = s
    d = t1 - t2
    den = 2 * M1 + M2 - M2 * math.cos(2 * d)
    a1 = (-G * (2 * M1 + M2) * math.sin(t1) - M2 * G * math.sin(t1 - 2 * t2)
          - 2 * math.sin(d) * M2 * (w2 * w2 * L2 + w1 * w1 * L1 * math.cos(d))) / (L1 * den)
    a2 = (2 * math.sin(d) * (w1 * w1 * L1 * (M1 + M2) + G * (M1 + M2) * math.cos(t1)
          + w2 * w2 * L2 * M2 * math.cos(d))) / (L2 * den)
    return w1, a1, w2, a2


def rk4(s: tuple[float, ...], dt: float) -> tuple[float, ...]:
    """One classic Runge–Kutta step."""
    def add(a, b, k):
        return tuple(x + k * y for x, y in zip(a, b))
    k1 = derivs(s)
    k2 = derivs(add(s, k1, dt / 2))
    k3 = derivs(add(s, k2, dt / 2))
    k4 = derivs(add(s, k3, dt))
    return tuple(x + dt / 6 * (a + 2 * b + 2 * c + d) for x, a, b, c, d in zip(s, k1, k2, k3, k4))


def energy(s: tuple[float, ...]) -> float:
    """Total mechanical energy (conserved up to integration error)."""
    t1, w1, t2, w2 = s
    v1sq = (L1 * w1) ** 2
    v2sq = v1sq + (L2 * w2) ** 2 + 2 * L1 * L2 * w1 * w2 * math.cos(t1 - t2)
    y1 = -L1 * math.cos(t1)
    y2 = y1 - L2 * math.cos(t2)
    return 0.5 * M1 * v1sq + 0.5 * M2 * v2sq + M1 * G * y1 + M2 * G * y2


def line(x0: int, y0: int, x1: int, y1: int) -> list[tuple[int, int]]:
    """Bresenham cells from (x0, y0) to (x1, y1)."""
    pts = []
    dx, dy = abs(x1 - x0), -abs(y1 - y0)
    sx, sy = (1 if x0 < x1 else -1), (1 if y0 < y1 else -1)
    err = dx + dy
    while True:
        pts.append((x0, y0))
        if x0 == x1 and y0 == y1:
            return pts
        e2 = 2 * err
        if e2 >= dy:
            err += dy
            x0 += sx
        if e2 <= dx:
            err += dx
            y0 += sy


def main(argv: list[str] | None = None) -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--frames", type=int, default=0)
    ap.add_argument("--width", type=int, default=72)
    ap.add_argument("--height", type=int, default=24)
    ap.add_argument("--fps", type=float, default=30)
    ap.add_argument("--theta1", type=float, default=120)
    ap.add_argument("--theta2", type=float, default=-10)
    ap.add_argument("--twin", action="store_true", help="add a second pendulum 0.01° apart")
    ap.add_argument("--no-color", action="store_true")
    a = ap.parse_args(argv)
    W, H = a.width, a.height
    states = [(math.radians(a.theta1), 0.0, math.radians(a.theta2), 0.0)]
    if a.twin:
        states.append((math.radians(a.theta1 + 0.01), 0.0, math.radians(a.theta2), 0.0))
    e0 = energy(states[0])
    trails: list[dict[tuple[int, int], int]] = [{} for _ in states]
    cx, cy = W // 2, H // 2
    scale_y = (H / 2 - 1) / (L1 + L2)
    scale_x = scale_y * 2.0  # terminal cells are about twice as tall as wide
    colors = ["\x1b[38;5;214m", "\x1b[38;5;45m"]
    frame = 0
    sys.stdout.write("\x1b[?25l\x1b[2J")
    try:
        while not a.frames or frame < a.frames:
            grid = [[" "] * W for _ in range(H)]
            col = [[-1] * W for _ in range(H)]
            for i, s in enumerate(states):
                for _ in range(8):
                    s = rk4(s, 1 / (a.fps * 8))
                states[i] = s
                t1, _, t2, _ = s
                x1, y1 = cx + L1 * math.sin(t1) * scale_x, cy + L1 * math.cos(t1) * scale_y
                x2, y2 = x1 + L2 * math.sin(t2) * scale_x, y1 + L2 * math.cos(t2) * scale_y
                p1, p2 = (round(x1), round(y1)), (round(x2), round(y2))
                tr = trails[i]
                for k in list(tr):
                    tr[k] -= 1
                    if tr[k] <= 0:
                        del tr[k]
                tr[p2] = len(TRAIL) * 6
                for (x, y), life in tr.items():
                    if 0 <= x < W and 0 <= y < H:
                        grid[y][x] = TRAIL[min(len(TRAIL) - 1, life // 6)]
                        col[y][x] = i
                for x, y in line(cx, cy, *p1)[1:-1] + line(*p1, *p2)[1:-1]:
                    if 0 <= x < W and 0 <= y < H:
                        grid[y][x] = "·"
                        col[y][x] = -1
                for (x, y), ch in ((p1, "o"), (p2, "O")):
                    if 0 <= x < W and 0 <= y < H:
                        grid[y][x] = ch
                        col[y][x] = i
            grid[cy][cx] = "+"
            out = []
            for y in range(H):
                if a.no_color:
                    out.append("".join(grid[y]))
                else:
                    out.append("".join((colors[c] if c >= 0 else "\x1b[0m") + ch for ch, c in zip(grid[y], col[y])) + "\x1b[0m")
            drift = abs(energy(states[0]) - e0) / abs(e0 or 1)
            out.append(f"frame {frame}  energy drift {drift:.2e}" + ("  (twin started 0.01° apart)" if a.twin else ""))
            sys.stdout.write("\x1b[H" + "\n".join(out))
            sys.stdout.flush()
            frame += 1
            time.sleep(1 / a.fps)
    except KeyboardInterrupt:
        pass
    finally:
        sys.stdout.write("\x1b[0m\x1b[?25h\n")


if __name__ == "__main__":
    main()
