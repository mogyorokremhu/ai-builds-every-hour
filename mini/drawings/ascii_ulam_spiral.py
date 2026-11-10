"""Ulam spiral: primes marked on a square spiral.
python ascii_ulam_spiral.py [size]"""
import sys


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    i = 2
    while i * i <= n:
        if n % i == 0:
            return False
        i += 1
    return True


def main(size: int = 35) -> None:
    grid = [[" "] * size for _ in range(size)]
    x = y = size // 2
    dx, dy = 1, 0  # right, then up, left, down
    n, seg, left = 1, 1, 1
    legs = 0
    while 0 <= x < size and 0 <= y < size:
        grid[y][x] = "#" if is_prime(n) else "."
        n += 1
        x, y = x + dx, y - dy
        left -= 1
        if left == 0:
            dx, dy = -dy, dx
            legs += 1
            if legs % 2 == 0:
                seg += 1
            left = seg
    print("\n".join(" ".join(r).rstrip() for r in grid))


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 35)
