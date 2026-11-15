"""Sierpinski triangle via Pascal's triangle mod 2.

Usage: python sierpinski_ascii.py [rows]   (default 32)
"""
import sys


def sierpinski(rows: int = 32) -> str:
    """Return the triangle as text; cell is '#' where C(n,k) is odd."""
    out = []
    for n in range(rows):
        cells = ["#" if (n & k) == k else " " for k in range(n + 1)]
        out.append(" " * (rows - n - 1) + " ".join(cells))
    return "\n".join(out)


if __name__ == "__main__":
    print(sierpinski(int(sys.argv[1]) if len(sys.argv) > 1 else 32))
