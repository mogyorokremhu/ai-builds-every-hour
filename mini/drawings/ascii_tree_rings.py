"""Cross-section of a tree trunk: wobbly growth rings."""
import math
import random

random.seed(7)
W, H = 72, 36
cx, cy = W / 2, H / 2
phases = [random.uniform(0, 6.28) for _ in range(3)]
shades = "#%=+-:."
for row in range(H):
    line = ""
    for col in range(W):
        dx, dy = (col - cx) / 2.0, row - cy
        ang = math.atan2(dy, dx)
        wob = 1 + 0.06 * math.sin(3 * ang + phases[0]) + 0.04 * math.sin(5 * ang + phases[1])
        rad = math.hypot(dx, dy) / wob
        if rad > 16:
            line += " "
        else:
            line += shades[int(rad * 1.3) % len(shades)]
    print(line.rstrip())
