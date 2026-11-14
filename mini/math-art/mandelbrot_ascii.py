"""Mandelbrot set rendered in the terminal with a character ramp.

Usage: python mandelbrot_ascii.py [width] [height] [max_iter]
"""
import sys

RAMP = " .:-=+*#%@"


def escape_time(c: complex, max_iter: int) -> int:
    """Iterations before |z| > 2 (max_iter if it never escapes)."""
    z = 0j
    for n in range(max_iter):
        z = z * z + c
        if abs(z) > 2:
            return n
    return max_iter


def render(width: int = 70, height: int = 24, max_iter: int = 60) -> str:
    rows = []
    for j in range(height):
        y = -1.2 + 2.4 * j / (height - 1)
        row = ""
        for i in range(width):
            x = -2.2 + 3.2 * i / (width - 1)
            n = escape_time(complex(x, y), max_iter)
            row += "@" if n == max_iter else RAMP[n * (len(RAMP) - 2) // max_iter + 1 if n else 0]
        rows.append(row)
    return "\n".join(rows)


if __name__ == "__main__":
    a = [int(v) for v in sys.argv[1:4]]
    print(render(*a))
