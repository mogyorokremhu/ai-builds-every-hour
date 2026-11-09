"""Vogel sunflower: seeds placed at the golden angle. python ascii_sunflower.py [seeds]"""
import math
import sys


def main(n: int = 900, w: int = 71, h: int = 35) -> None:
    grid = [[" "] * w for _ in range(h)]
    golden = math.pi * (3 - math.sqrt(5))
    for i in range(n):
        r = math.sqrt(i / n)
        a = i * golden
        x = int(w / 2 + r * (w / 2 - 1) * math.cos(a))
        y = int(h / 2 + r * (h / 2 - 1) * math.sin(a))
        grid[y][x] = ".o*@"[min(3, int(4 * (1 - r)))] if r < 0.98 else "."
    print("\n".join("".join(row).rstrip() for row in grid))


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 900)
