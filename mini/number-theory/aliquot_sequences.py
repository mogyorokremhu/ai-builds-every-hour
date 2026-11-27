"""Aliquot sequences: iterate s(n) = sigma(n) - n (python aliquot_sequences.py 220 276)."""
import sys


def proper_divisor_sum(n: int) -> int:
    """Sum of proper divisors of n."""
    if n < 2:
        return 0
    total, i = 1, 2
    while i * i <= n:
        if n % i == 0:
            total += i
            if i != n // i:
                total += n // i
        i += 1
    return total


def aliquot(n: int, limit: int = 30, cap: int = 10**10) -> list[int]:
    """Follow the aliquot sequence from n until it ends, cycles, or hits limit/cap."""
    seq = [n]
    while len(seq) < limit and seq[-1] != 0:
        nxt = proper_divisor_sum(seq[-1])
        seq.append(nxt)
        if nxt in seq[:-1] or nxt > cap:
            break
    return seq


def classify(seq: list[int]) -> str:
    """Describe how a sequence ended."""
    if seq[-1] == 0:
        return "terminates at 0"
    if seq[-1] in seq[:-1]:
        period = len(seq) - 1 - seq.index(seq[-1])
        return {1: "perfect number", 2: "amicable pair"}.get(period, f"sociable cycle of length {period}")
    return "unresolved within limit"


if __name__ == "__main__":
    for arg in sys.argv[1:] or ["6", "220", "12496", "27"]:
        s = aliquot(int(arg))
        print(f"{arg}: {s[:12]}{'...' if len(s) > 12 else ''} -> {classify(s)}")
