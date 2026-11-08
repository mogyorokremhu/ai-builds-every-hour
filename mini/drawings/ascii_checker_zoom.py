"""Rotating, zooming checkerboard frames side by side. Usage: python ascii_checker_zoom.py [frames]"""
import math
import sys


def frame(t, w=24, h=12):
    ang, zoom = t * 0.5, 1 + t * 0.35
    rows = []
    for j in range(h):
        row = ""
        for i in range(w):
            x, y = (i - w / 2) / zoom, (j - h / 2) * 2 / zoom
            u = x * math.cos(ang) - y * math.sin(ang)
            v = x * math.sin(ang) + y * math.cos(ang)
            row += "█" if (math.floor(u / 2) + math.floor(v / 2)) % 2 == 0 else " "
        rows.append(row)
    return rows


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    frames = [frame(t) for t in range(n)]
    for lines in zip(*frames):
        print(" | ".join(lines))
