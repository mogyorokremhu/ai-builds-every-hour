"""Ulam spiral: print primes on a square spiral as ASCII."""
import sys


def primes_upto(n: int) -> list[bool]:
    """Sieve of Eratosthenes; returns a primality table up to n."""
    s = [True] * (n + 1)
    s[0:2] = [False, False][: min(2, n + 1)]
    for i in range(2, int(n ** 0.5) + 1):
        if s[i]:
            s[i * i :: i] = [False] * len(s[i * i :: i])
    return s


def ulam(size: int) -> list[str]:
    """Return rows of an Ulam spiral of odd/even size x size."""
    is_p = primes_upto(size * size)
    grid = [[" "] * size for _ in range(size)]
    x = y = size // 2
    dx, dy = 1, 0
    steps, n = 1, 1
    while n <= size * size:
        for _ in range(2):
            for _ in range(steps):
                if 0 <= x < size and 0 <= y < size and n <= size * size:
                    grid[y][x] = "#" if is_p[n] else "."
                n += 1
                x, y = x + dx, y + dy
            dx, dy = -dy, dx
        steps += 1
    return ["".join(r) for r in grid]


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 31
    print("\n".join(ulam(n)))
