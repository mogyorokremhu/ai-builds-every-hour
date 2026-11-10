#!/usr/bin/env python3
"""Boids flocking: separation, alignment and cohesion on a wrapping field.

Usage: python boids.py [--frames N] [--boids 30] [--fps 20] [--seed S]
"""
import argparse
import math
import random
import sys
import time

W, H = 60, 20
ARROWS = ">v<^"


def step(bs):
    out = []
    for i, (x, y, vx, vy) in enumerate(bs):
        sx = sy = ax = ay = cx = cy = n = 0
        for j, (ox, oy, ovx, ovy) in enumerate(bs):
            if i == j:
                continue
            dx = (ox - x + W / 2) % W - W / 2
            dy = (oy - y + H / 2) % H - H / 2
            d = math.hypot(dx, dy)
            if d < 10:
                n += 1
                ax += ovx; ay += ovy; cx += dx; cy += dy
                if d < 2.5:
                    sx -= dx; sy -= dy
        if n:
            vx += 0.05 * (ax / n - vx) + 0.01 * cx / n + 0.08 * sx
            vy += 0.05 * (ay / n - vy) + 0.01 * cy / n + 0.08 * sy
        sp = math.hypot(vx, vy) or 1
        if sp > 1: vx, vy = vx / sp, vy / sp
        out.append(((x + vx) % W, (y + vy * 0.6) % H, vx, vy))
    return out


def render(bs):
    g = [[" "] * W for _ in range(H)]
    for x, y, vx, vy in bs:
        a = math.atan2(vy, vx)
        g[int(y)][int(x)] = ARROWS[int(((a + math.pi / 4) % (2 * math.pi)) // (math.pi / 2)) % 4]
    return "\n".join("".join(r) for r in g)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--frames", type=int, default=150)
    p.add_argument("--boids", type=int, default=30)
    p.add_argument("--fps", type=float, default=20)
    p.add_argument("--seed", type=int, default=1)
    a = p.parse_args()
    r = random.Random(a.seed)
    bs = [(r.uniform(0, W), r.uniform(0, H), r.uniform(-1, 1), r.uniform(-1, 1)) for _ in range(a.boids)]
    for _ in range(a.frames):
        sys.stdout.write("\x1b[H\x1b[2J" + render(bs) + "\n")
        sys.stdout.flush()
        bs = step(bs)
        time.sleep(1 / a.fps)


if __name__ == "__main__":
    main()
