"""Population-count and bit-twiddling tricks with self-checks."""


def popcount_loop(n: int) -> int:
    c = 0
    while n:
        n &= n - 1  # clear lowest set bit
        c += 1
    return c


def popcount_swar(n: int) -> int:
    """SWAR popcount for 32-bit values."""
    n &= 0xFFFFFFFF
    n = n - ((n >> 1) & 0x55555555)
    n = (n & 0x33333333) + ((n >> 2) & 0x33333333)
    n = (n + (n >> 4)) & 0x0F0F0F0F
    return ((n * 0x01010101) & 0xFFFFFFFF) >> 24


def is_power_of_two(n: int) -> bool:
    return n > 0 and n & (n - 1) == 0


def lowest_set_bit(n: int) -> int:
    return n & -n


def reverse_bits32(n: int) -> int:
    return int(f"{n & 0xFFFFFFFF:032b}"[::-1], 2)


def next_power_of_two(n: int) -> int:
    return 1 if n <= 1 else 1 << (n - 1).bit_length()


if __name__ == "__main__":
    for n in (0, 1, 7, 255, 0xDEADBEEF):
        assert popcount_loop(n) == popcount_swar(n) == bin(n).count("1")
    assert is_power_of_two(64) and not is_power_of_two(65)
    assert lowest_set_bit(0b101000) == 0b1000
    assert reverse_bits32(1) == 1 << 31
    assert next_power_of_two(100) == 128
    print("all bit tricks OK; popcount(0xDEADBEEF) =", popcount_swar(0xDEADBEEF))
