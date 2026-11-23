"""Gosper's hack: iterate all n-bit integers with exactly k set bits, in order."""
import sys
from itertools import combinations


def gosper(n: int, k: int):
    """Yield every integer < 2**n with exactly k bits set, ascending."""
    if k == 0:
        yield 0
        return
    x = (1 << k) - 1
    while x < (1 << n):
        yield x
        c = x & -x
        r = x + c
        x = (((r ^ x) >> 2) // c) | r


if __name__ == "__main__":
    n, k = (int(a) for a in sys.argv[1:3]) if len(sys.argv) > 2 else (5, 2)
    got = list(gosper(n, k))
    want = sorted(sum(1 << i for i in c) for c in combinations(range(n), k))
    assert got == want
    for v in got:
        print(f"{v:0{n}b}")
    print(f"{len(got)} values OK")
