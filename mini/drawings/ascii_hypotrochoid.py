"""Hypotrochoid (spirograph-style) curve plotted in ASCII."""
import math

W, H = 70, 34
R, r, d = 5.0, 3.0, 4.0
grid = [[" "] * W for _ in range(H)]
extent = (R - r) + d
for i in range(4000):
    t = i * 2 * math.pi / 500
    x = (R - r) * math.cos(t) + d * math.cos((R - r) / r * t)
    y = (R - r) * math.sin(t) - d * math.sin((R - r) / r * t)
    col = int((x / extent + 1) / 2 * (W - 1))
    row = int((y / extent + 1) / 2 * (H - 1))
    grid[row][col] = "*"
print("\n".join("".join(line).rstrip() for line in grid))
