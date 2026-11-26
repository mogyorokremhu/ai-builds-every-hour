"""Perspective starfield: stars streak outward from the centre."""
import math
import random

random.seed(3)
W, H = 78, 32
cx, cy = W / 2, H / 2
grid = [[" "] * W for _ in range(H)]
for _ in range(220):
    ang = random.uniform(0, 6.2832)
    depth = random.uniform(0.05, 1.0)
    dist = (1 - depth) * 30
    steps = int(3 + (1 - depth) * 6)
    for s in range(steps):
        d = dist - s * 0.8
        if d < 0:
            break
        x, y = int(cx + math.cos(ang) * d * 1.9), int(cy + math.sin(ang) * d * 0.9)
        if 0 <= x < W and 0 <= y < H:
            grid[y][x] = "*" if s == 0 and depth < 0.5 else ("." if s else "+")
print("\n".join("".join(r).rstrip() for r in grid))
