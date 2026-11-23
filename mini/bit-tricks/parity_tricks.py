"""Parity of a word: loop, xor-fold, lookup table; plus Hamming(7,4) syndrome."""


def parity_loop(x: int) -> int:
    p = 0
    while x:
        p ^= 1
        x &= x - 1
    return p


def parity_fold(x: int) -> int:
    x &= 0xFFFFFFFF
    for s in (16, 8, 4, 2, 1):
        x ^= x >> s
    return x & 1


def hamming74_encode(d: int) -> int:
    d1, d2, d3, d4 = (d >> 3) & 1, (d >> 2) & 1, (d >> 1) & 1, d & 1
    p1, p2, p4 = d1 ^ d2 ^ d4, d1 ^ d3 ^ d4, d2 ^ d3 ^ d4
    bits = [p1, p2, d1, p4, d2, d3, d4]  # positions 1..7
    return sum(b << i for i, b in enumerate(bits))


def hamming74_syndrome(w: int) -> int:
    """0 if valid, otherwise the 1-based position of the flipped bit."""
    s = 0
    for pos in range(1, 8):
        if (w >> (pos - 1)) & 1:
            s ^= pos
    return s


if __name__ == "__main__":
    for x in (0, 1, 7, 0xFF, 0xDEADBEEF):
        assert parity_loop(x) == parity_fold(x) == bin(x).count("1") % 2
    for d in range(16):
        w = hamming74_encode(d)
        assert hamming74_syndrome(w) == 0
        for pos in range(7):
            assert hamming74_syndrome(w ^ (1 << pos)) == pos + 1
    print("parity and Hamming(7,4) single-error correction OK")
