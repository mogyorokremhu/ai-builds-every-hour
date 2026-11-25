"""Gray code generation and conversion, with adjacency check."""


def to_gray(n: int) -> int:
    return n ^ (n >> 1)


def from_gray(g: int) -> int:
    n = 0
    while g:
        n ^= g
        g >>= 1
    return n


def sequence(bits: int) -> list[str]:
    return [format(to_gray(i), f"0{bits}b") for i in range(1 << bits)]


if __name__ == "__main__":
    seq = sequence(4)
    print(" ".join(seq))
    for a, b in zip(seq, seq[1:] + seq[:1]):
        assert sum(x != y for x, y in zip(a, b)) == 1  # cyclic single-bit change
    assert all(from_gray(to_gray(i)) == i for i in range(1024))
    print("ok")
