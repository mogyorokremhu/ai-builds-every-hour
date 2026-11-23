"""Symmetric random pixel sprites (invader-style) in ASCII.
Usage: python pixel_sprite.py [count] [seed] [size]"""
import random
import sys


def sprite(size: int, rng: random.Random) -> list[str]:
    """Build a left-right symmetric sprite of size x size."""
    half = (size + 1) // 2
    rows = []
    for _ in range(size):
        left = [rng.random() < 0.5 for _ in range(half)]
        full = left + left[: size // 2][::-1]
        rows.append("".join("██" if b else "  " for b in full))
    return rows


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    rng = random.Random(int(sys.argv[2]) if len(sys.argv) > 2 else None)
    size = int(sys.argv[3]) if len(sys.argv) > 3 else 7
    for _ in range(n):
        print("\n".join(sprite(size, rng)))
        print()
