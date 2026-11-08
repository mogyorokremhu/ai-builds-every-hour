"""Classic demo-scene plasma rendered as shaded ASCII. Usage: python ascii_plasma.py [t]"""
import math
import sys

SHADES = " .:-=+*#%@"


def plasma(x, y, t):
    v = math.sin(x / 5 + t) + math.sin(y / 3 - t * 0.7)
    v += math.sin((x + y) / 7 + t * 0.5) + math.sin(math.hypot(x - 40, (y - 12) * 2) / 4 - t)
    return (v + 4) / 8


def main():
    t = float(sys.argv[1]) if len(sys.argv) > 1 else 1.0
    for y in range(25):
        print("".join(SHADES[min(9, int(plasma(x, y, t) * 10))] for x in range(80)))


if __name__ == "__main__":
    main()
