"""Recamán's sequence: a(n) = a(n-1) - n if positive and unseen, else a(n-1) + n."""


def recaman(count: int) -> list[int]:
    """Return the first `count` terms starting at a(0)=0."""
    seq, seen = [0], {0}
    for n in range(1, count):
        v = seq[-1] - n
        if v < 0 or v in seen:
            v = seq[-1] + n
        seq.append(v)
        seen.add(v)
    return seq


def first_repeat(limit: int = 1000) -> int:
    """Return the first value that appears twice."""
    seen: set[int] = set()
    for v in recaman(limit):
        if v in seen:
            return v
        seen.add(v)
    raise ValueError("no repeat found")


if __name__ == "__main__":
    assert recaman(10) == [0, 1, 3, 6, 2, 7, 13, 20, 12, 21]
    assert first_repeat() == 42
    print(recaman(20))
    print("first repeated value:", first_repeat())
