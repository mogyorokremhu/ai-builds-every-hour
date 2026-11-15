"""Render a Julia set as ASCII art for a chosen constant c."""
import sys

CHARS = " .:-=+*#%@"


def julia(c: complex, w: int = 70, h: int = 24, limit: int = 50) -> str:
    rows = []
    for y in range(h):
        row = ""
        for x in range(w):
            z = complex(-1.6 + 3.2 * x / w, -1.1 + 2.2 * y / h)
            n = 0
            while n < limit and abs(z) <= 2:
                z = z * z + c
                n += 1
            row += CHARS[n * (len(CHARS) - 1) // limit]
        rows.append(row)
    return "\n".join(rows)


if __name__ == "__main__":
    c = complex(sys.argv[1]) if len(sys.argv) > 1 else complex(-0.8, 0.156)
    print(julia(c))
