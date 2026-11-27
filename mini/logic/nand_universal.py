"""Build NOT/AND/OR/XOR from NAND only and verify against Python operators."""
from itertools import product


def nand(a: bool, b: bool) -> bool:
    return not (a and b)


def n_not(a): return nand(a, a)
def n_and(a, b): return n_not(nand(a, b))
def n_or(a, b): return nand(n_not(a), n_not(b))
def n_xor(a, b):
    m = nand(a, b)
    return nand(nand(a, m), nand(b, m))


if __name__ == "__main__":
    for a, b in product([False, True], repeat=2):
        assert n_and(a, b) == (a and b)
        assert n_or(a, b) == (a or b)
        assert n_xor(a, b) == (a != b)
        assert n_not(a) == (not a)
    print("NAND is universal: ok")
