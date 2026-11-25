"""Look-and-say sequence (1, 11, 21, 1211, ...) and Conway's growth constant."""
from itertools import groupby


def next_term(s: str) -> str:
    """Describe the runs of digits in s."""
    return "".join(f"{len(list(g))}{d}" for d, g in groupby(s))


def terms(n: int, start: str = "1") -> list[str]:
    """Return the first n terms."""
    out = [start]
    for _ in range(n - 1):
        out.append(next_term(out[-1]))
    return out


if __name__ == "__main__":
    t = terms(6)
    assert t == ["1", "11", "21", "1211", "111221", "312211"]
    big = terms(31)
    ratio = len(big[-1]) / len(big[-2])
    assert 1.28 < ratio < 1.31
    print(t)
    print("length ratio at term 31:", round(ratio, 4), "(Conway ~1.3036)")
