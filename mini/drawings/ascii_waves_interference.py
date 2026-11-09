"""Ripples from three point sources adding up (python ascii_waves_interference.py)."""
import math

SH = " .:-=+*#%@"
SRC = [(15, 8), (45, 8), (30, 18)]
for y in range(26):
    row = ""
    for x in range(61):
        v = sum(math.sin(math.hypot(x - sx, (y - sy) * 2) * 0.9) for sx, sy in SRC) / 3
        row += SH[int((v + 1) / 2 * 9.99)]
    print(row)
