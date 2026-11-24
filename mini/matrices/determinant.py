"""Exact determinant via fraction-based Gaussian elimination."""
from fractions import Fraction


def det(m: list[list]) -> Fraction:
    """Determinant of a square matrix using exact arithmetic."""
    a = [[Fraction(x) for x in row] for row in m]
    n = len(a)
    d = Fraction(1)
    for c in range(n):
        p = next((r for r in range(c, n) if a[r][c] != 0), None)
        if p is None:
            return Fraction(0)
        if p != c:
            a[c], a[p] = a[p], a[c]
            d = -d
        d *= a[c][c]
        for r in range(c + 1, n):
            f = a[r][c] / a[c][c]
            for k in range(c, n):
                a[r][k] -= f * a[c][k]
    return d


if __name__ == "__main__":
    assert det([[1, 2], [3, 4]]) == -2
    assert det([[2, 0, 1], [1, 3, 2], [1, 1, 1]]) == 2 * (3 - 2) - 0 + 1 * (1 - 3)
    assert det([[1, 2], [2, 4]]) == 0
    print("det([[1,2],[3,4]]) =", det([[1, 2], [3, 4]]))
    print("ok")
