"""Next lexicographic bit permutation and subset enumeration of a mask."""


def next_perm(v: int) -> int:
    """Next integer with the same popcount (Gosper-style via trailing zeros)."""
    t = v | (v - 1)
    return (t + 1) | (((~t & -~t) - 1) >> (((v & -v).bit_length() - 1) + 1))


def submasks(mask: int):
    """Yield every submask of mask in descending order, ending with 0."""
    s = mask
    while True:
        yield s
        if s == 0:
            return
        s = (s - 1) & mask


if __name__ == "__main__":
    v = 0b0111
    seq = [v]
    for _ in range(5):
        v = next_perm(v)
        seq.append(v)
    print([bin(x) for x in seq])
    assert all(bin(x).count("1") == 3 for x in seq)
    subs = list(submasks(0b1011))
    print([bin(s) for s in subs])
    assert len(subs) == 8 and len(set(subs)) == 8
    print("ok")
