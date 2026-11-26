"""Trace, Frobenius norm, and row/column sum norms of a matrix."""
from math import sqrt


def trace(m):
    return sum(m[i][i] for i in range(min(len(m), len(m[0]))))


def frobenius(m):
    return sqrt(sum(x * x for r in m for x in r))


def norm_1(m):
    """Max absolute column sum."""
    return max(sum(abs(r[j]) for r in m) for j in range(len(m[0])))


def norm_inf(m):
    """Max absolute row sum."""
    return max(sum(abs(x) for x in r) for r in m)


if __name__ == "__main__":
    a = [[1, -2], [3, 4]]
    assert trace(a) == 5
    assert abs(frobenius(a) - sqrt(30)) < 1e-12
    assert norm_1(a) == 6 and norm_inf(a) == 7
    print("trace", trace(a), "frobenius", round(frobenius(a), 4), "1-norm", norm_1(a), "inf-norm", norm_inf(a))
