"""Leap-year utilities: counting, listing and next-leap lookups."""


def is_leap(y: int) -> bool:
    return y % 4 == 0 and (y % 100 != 0 or y % 400 == 0)


def count_leaps(a: int, b: int) -> int:
    """Leap years in the inclusive range [a, b], in O(1)."""
    def upto(y: int) -> int:
        return y // 4 - y // 100 + y // 400
    return upto(b) - upto(a - 1)


def next_leap(y: int) -> int:
    y += 1
    while not is_leap(y):
        y += 1
    return y


if __name__ == "__main__":
    assert count_leaps(1900, 2000) == sum(is_leap(y) for y in range(1900, 2001)) == 25
    assert next_leap(2096) == 2104
    print("leap years 2020-2040:", [y for y in range(2020, 2041) if is_leap(y)])
    print("next leap after 2026:", next_leap(2026))
