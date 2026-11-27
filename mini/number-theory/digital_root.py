"""Digital roots, persistence and Harshad (Niven) numbers."""
import sys


def digit_sum(n: int) -> int:
    return sum(int(c) for c in str(n))


def digital_root(n: int) -> int:
    """Repeated digit sum until one digit (closed form for n > 0)."""
    return 0 if n == 0 else 1 + (n - 1) % 9


def persistence(n: int) -> int:
    """Multiplicative persistence: steps of multiplying digits until one digit."""
    steps = 0
    while n >= 10:
        p = 1
        for c in str(n):
            p *= int(c)
        n, steps = p, steps + 1
    return steps


def harshad(limit: int) -> list[int]:
    """Numbers divisible by their digit sum."""
    return [n for n in range(1, limit) if n % digit_sum(n) == 0]


if __name__ == "__main__":
    limit = int(sys.argv[1]) if len(sys.argv) > 1 else 100
    for n in range(1, 2000):
        r = n
        while r >= 10:
            r = digit_sum(r)
        assert r == digital_root(n)
    print("digital root closed form verified to 2000")
    print("persistence of 277777788888899:", persistence(277777788888899))
    print(f"Harshad numbers below {limit}:", harshad(limit))
