"""Print an ASCII/ANSI hue wheel with HSV colouring.

Usage: python color_wheel_ascii.py [radius]
"""
import colorsys
import math
import sys


def wheel(radius: int = 10) -> list[str]:
    rows = []
    for y in range(-radius, radius + 1):
        row = ""
        for x in range(-radius * 2, radius * 2 + 1):
            d = math.hypot(x / 2, y)
            if d > radius:
                row += " "
                continue
            hue = (math.atan2(-y, x / 2) / (2 * math.pi)) % 1.0
            r, g, b = (round(255 * v) for v in colorsys.hsv_to_rgb(hue, d / radius, 1.0))
            row += f"\x1b[48;2;{r};{g};{b}m \x1b[0m"
        rows.append(row)
    return rows


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    assert len(wheel(3)) == 7
    print("\n".join(wheel(n)))
