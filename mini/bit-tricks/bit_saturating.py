"""Saturating and wrapping arithmetic on fixed-width unsigned/signed integers.

Usage: python bit_saturating.py
"""


def wrap_u(x: int, bits: int) -> int:
    return x & ((1 << bits) - 1)


def wrap_s(x: int, bits: int) -> int:
    x = wrap_u(x, bits)
    return x - (1 << bits) if x >> (bits - 1) else x


def sat_add_u(a: int, b: int, bits: int = 8) -> int:
    return min(a + b, (1 << bits) - 1)


def sat_sub_u(a: int, b: int, bits: int = 8) -> int:
    return max(a - b, 0)


def sat_add_s(a: int, b: int, bits: int = 8) -> int:
    lo, hi = -(1 << (bits - 1)), (1 << (bits - 1)) - 1
    return max(lo, min(hi, a + b))


def overflowed_s(a: int, b: int, bits: int = 8) -> bool:
    """Signed add overflow: operands share a sign that the result lacks."""
    r = wrap_s(a + b, bits)
    return (a < 0) == (b < 0) and (r < 0) != (a < 0)


if __name__ == "__main__":
    print("u8 200+100 wrap:", wrap_u(200 + 100, 8), " sat:", sat_add_u(200, 100))
    print("u8 10-20  sat:", sat_sub_u(10, 20))
    print("s8 100+100 wrap:", wrap_s(200, 8), " sat:", sat_add_s(100, 100))
    print("s8 -100-100 sat:", sat_add_s(-100, -100))
    print("overflow 100+100:", overflowed_s(100, 100), " 100+(-100):", overflowed_s(100, -100))
