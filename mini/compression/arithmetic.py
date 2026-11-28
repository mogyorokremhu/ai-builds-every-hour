"""Arithmetic coding with exact fractions: encode a string as one rational number."""
from fractions import Fraction
from collections import Counter


def model(text: str) -> dict[str, tuple[Fraction, Fraction]]:
    """Map each symbol to its [low, high) slice of [0, 1)."""
    counts, total, low, table = Counter(text), len(text), Fraction(0), {}
    for sym in sorted(counts):
        high = low + Fraction(counts[sym], total)
        table[sym] = (low, high)
        low = high
    return table


def encode(text: str, table) -> Fraction:
    low, high = Fraction(0), Fraction(1)
    for ch in text:
        span = high - low
        lo, hi = table[ch]
        low, high = low + span * lo, low + span * hi
    return (low + high) / 2


def decode(code: Fraction, table, n: int) -> str:
    out = []
    for _ in range(n):
        for sym, (lo, hi) in table.items():
            if lo <= code < hi:
                out.append(sym)
                code = (code - lo) / (hi - lo)
                break
    return "".join(out)


if __name__ == "__main__":
    text = "abracadabra"
    table = model(text)
    code = encode(text, table)
    print("code =", code, f"({code.denominator.bit_length()} bits denominator)")
    assert decode(code, table, len(text)) == text
    print("round trip ok")
