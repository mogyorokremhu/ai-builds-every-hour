"""Moire: two line gratings, one slightly rotated.  python ascii_moire_grid.py [degrees]"""
import math, sys

def main(deg: float = 4.0, w: int = 76, h: int = 30) -> None:
    t = math.radians(deg)
    for y in range(h):
        row = ""
        for x in range(w):
            px, py = x / 2, y
            a = math.sin(px * 2.2)
            b = math.sin((px * math.cos(t) - py * math.sin(t)) * 2.2)
            v = a * b
            row += "#" if v > 0.6 else "+" if v > 0.1 else "." if v > -0.4 else " "
        print(row)

if __name__ == "__main__":
    main(float(sys.argv[1]) if len(sys.argv) > 1 else 4.0)
