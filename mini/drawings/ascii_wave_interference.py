"""Interference pattern of two point wave sources, shaded with ASCII."""
import math

SHADES = " .:-=+*#%@"
S1, S2 = (20, 10), (40, 10)
for y in range(21):
    row = ""
    for x in range(61):
        v = sum(math.sin(math.hypot(x - sx, (y - sy) * 2) * 0.9) for sx, sy in (S1, S2))
        row += SHADES[min(9, int((v + 2) / 4 * 10))]
    print(row)
