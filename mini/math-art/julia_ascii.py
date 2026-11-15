"""Julia set rendered in the terminal.

Usage: python julia_ascii.py [re im]   (default c = -0.8+0.156i)
"""
import sys

RAMP = " .:-=+*#%@"


def julia(c: complex, width: int = 70, height: int = 26, max_iter: int = 50) -> str:
    rows = []
    for j in range(height):
        y = 1.2 - 2.4 * j / (height - 1)
        row = []
        for i in range(width):
            z = complex(-1.6 + 3.2 * i / (width - 1), y)
            n = 0
            while n < max_iter and abs(z) <= 2:
                z = z * z + c
                n += 1
            row.append(RAMP[min(len(RAMP) - 1, n * len(RAMP) // (max_iter + 1))])
        rows.append("".join(row))
    return "\n".join(rows)


if __name__ == "__main__":
    c = complex(float(sys.argv[1]), float(sys.argv[2])) if len(sys.argv) >= 3 else complex(-0.8, 0.156)
    print(julia(c))
