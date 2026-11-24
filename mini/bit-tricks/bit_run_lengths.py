"""Run-length tricks on bits: longest run of ones, run count, leading/trailing zeros."""


def longest_ones(x: int) -> int:
    n = 0
    while x:
        x &= x << 1
        n += 1
    return n


def run_count(x: int) -> int:
    """Number of maximal runs of 1 bits."""
    return bin(x & ~(x << 1)).count("1")


def trailing_zeros(x: int) -> int:
    return (x & -x).bit_length() - 1 if x else -1


def leading_zeros(x: int, width: int = 32) -> int:
    return width - x.bit_length()


if __name__ == "__main__":
    x = 0b1101110010
    print(bin(x), longest_ones(x), run_count(x), trailing_zeros(x), leading_zeros(x, 16))
    assert longest_ones(x) == 3 and run_count(x) == 3
    assert trailing_zeros(0b1000) == 3 and leading_zeros(1, 8) == 7
    print("ok")
