"""Lorenz attractor projected onto the x-z plane as a density plot. Usage: python ascii_lorenz.py [steps]"""
import sys

SHADES = " .:+*#@"


def main():
    steps = int(sys.argv[1]) if len(sys.argv) > 1 else 40000
    w, h = 78, 30
    grid = [[0] * w for _ in range(h)]
    x, y, z = 1.0, 1.0, 1.0
    dt, s, r, b = 0.005, 10.0, 28.0, 8 / 3
    for i in range(steps):
        x, y, z = x + s * (y - x) * dt, y + (x * (r - z) - y) * dt, z + (x * y - b * z) * dt
        if i > 200:
            cx, cy = int((x + 22) / 44 * (w - 1)), int((50 - z) / 50 * (h - 1))
            if 0 <= cx < w and 0 <= cy < h:
                grid[cy][cx] += 1
    top = max(max(row) for row in grid) or 1
    for row in grid:
        print("".join(SHADES[min(6, int(c / top * 7 ** 0.5 * 2.6))] if c else " " for c in row))


if __name__ == "__main__":
    main()
