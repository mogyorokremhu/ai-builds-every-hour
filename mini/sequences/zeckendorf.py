"""Zeckendorf representation: every positive integer is a unique sum of non-consecutive Fibonacci numbers."""


def fibs_upto(n: int) -> list[int]:
    """Fibonacci numbers 1, 2, 3, 5, ... not exceeding n."""
    a, b, out = 1, 2, []
    while a <= n:
        out.append(a)
        a, b = b, a + b
    return out


def zeckendorf(n: int) -> list[int]:
    """Greedy decomposition of n into non-consecutive Fibonacci numbers (descending)."""
    parts = []
    for f in reversed(fibs_upto(n)):
        if f <= n:
            parts.append(f)
            n -= f
    return parts


def to_bits(n: int) -> str:
    """Zeckendorf digit string, most significant first."""
    fs = fibs_upto(n)
    used = set(zeckendorf(n))
    return "".join("1" if f in used else "0" for f in reversed(fs))


if __name__ == "__main__":
    assert zeckendorf(100) == [89, 8, 3]
    assert to_bits(12) == "10101"
    for k in range(1, 500):
        assert sum(zeckendorf(k)) == k and "11" not in to_bits(k)
    for k in range(1, 21):
        print(k, to_bits(k))
