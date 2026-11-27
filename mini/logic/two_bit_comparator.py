"""Gate-level 2-bit comparator (A>B, A==B, A<B) checked over all 16 inputs."""
from itertools import product


def compare(a1: int, a0: int, b1: int, b0: int) -> tuple[int, int, int]:
    eq1 = 1 - (a1 ^ b1)
    eq0 = 1 - (a0 ^ b0)
    gt = (a1 & (1 - b1)) | (eq1 & a0 & (1 - b0))
    eq = eq1 & eq0
    lt = (1 - a1) & b1 | (eq1 & (1 - a0) & b0)
    return gt, eq, lt


if __name__ == "__main__":
    for a1, a0, b1, b0 in product((0, 1), repeat=4):
        a, b = a1 * 2 + a0, b1 * 2 + b0
        assert compare(a1, a0, b1, b0) == (int(a > b), int(a == b), int(a < b))
    print("2-bit comparator: all 16 cases ok")
