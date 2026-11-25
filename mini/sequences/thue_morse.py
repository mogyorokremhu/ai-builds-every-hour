"""Thue-Morse sequence: bit-count parity, substitution form, and square-freeness check."""


def thue_morse(n: int) -> list[int]:
    """First n terms: t(i) = parity of popcount(i)."""
    return [bin(i).count("1") & 1 for i in range(n)]


def by_substitution(rounds: int) -> list[int]:
    """Build via 0 -> 01, 1 -> 10 repeated `rounds` times."""
    seq = [0]
    for _ in range(rounds):
        seq = [b for x in seq for b in (x, 1 - x)]
    return seq


def has_cube(seq: list[int]) -> bool:
    """True if some block repeats three times in a row (Thue-Morse has none)."""
    n = len(seq)
    for size in range(1, n // 3 + 1):
        for i in range(n - 3 * size + 1):
            if seq[i:i + size] == seq[i + size:i + 2 * size] == seq[i + 2 * size:i + 3 * size]:
                return True
    return False


if __name__ == "__main__":
    assert thue_morse(8) == [0, 1, 1, 0, 1, 0, 0, 1]
    assert by_substitution(5) == thue_morse(32)
    assert not has_cube(thue_morse(64))
    print("".join(map(str, thue_morse(32))))
