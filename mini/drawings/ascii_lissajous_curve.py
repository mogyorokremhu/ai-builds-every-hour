"""ASCII Lissajous curve drawn on a character grid."""
import math

W, H = 61, 27
A, B, DELTA = 3, 2, math.pi / 2
grid = [[" "] * W for _ in range(H)]
for i in range(2000):
    t = i / 2000 * 2 * math.pi
    x = int((math.sin(A * t + DELTA) + 1) / 2 * (W - 1))
    y = int((math.sin(B * t) + 1) / 2 * (H - 1))
    grid[y][x] = "*"
print("\n".join("".join(r) for r in grid))
