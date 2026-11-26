"""Powers of two: test, round up/down, log2, and lowest/highest set bit.

Usage: python bit_next_pow2.py [n ...]
"""
import sys


def is_pow2(n: int) -> bool:
    return n > 0 and n & (n - 1) == 0


def next_pow2(n: int) -> int:
    """Smallest power of two >= n (1 for n <= 1)."""
    if n <= 1:
        return 1
    return 1 << (n - 1).bit_length()


def prev_pow2(n: int) -> int:
    """Largest power of two <= n (n >= 1)."""
    return 1 << (n.bit_length() - 1)


def lowest_set(n: int) -> int:
    return n & -n


def floor_log2(n: int) -> int:
    return n.bit_length() - 1


if __name__ == "__main__":
    nums = [int(a) for a in sys.argv[1:]] or [1, 5, 16, 17, 100, 1023]
    print(f"{'n':>6} {'pow2?':>6} {'next':>6} {'prev':>6} {'low':>5} {'log2':>5}")
    for n in nums:
        print(f"{n:>6} {str(is_pow2(n)):>6} {next_pow2(n):>6} {prev_pow2(n):>6} "
              f"{lowest_set(n):>5} {floor_log2(n):>5}")
