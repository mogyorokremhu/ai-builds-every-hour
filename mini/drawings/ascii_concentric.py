"""Moire-like concentric rings from two centres: python ascii_concentric.py [spacing]"""
import math, sys

def draw(w=70, h=30, k=2.0):
    chars = " .:-=+*#%@"
    for y in range(h):
        line = ""
        for x in range(w):
            d1 = math.hypot((x - w * 0.35) / 2, y - h / 2)
            d2 = math.hypot((x - w * 0.65) / 2, y - h / 2)
            v = (math.sin(d1 * k) + math.sin(d2 * k)) / 4 + 0.5
            line += chars[min(9, int(v * 10))]
        print(line)

if __name__ == "__main__":
    draw(k=float(sys.argv[1]) if len(sys.argv) > 1 else 2.0)
