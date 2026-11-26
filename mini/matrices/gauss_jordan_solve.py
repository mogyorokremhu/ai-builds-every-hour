"""Solve linear systems exactly with Gauss-Jordan elimination over fractions."""
from fractions import Fraction


def solve(a, b):
    n = len(a)
    m = [[Fraction(x) for x in row] + [Fraction(bi)] for row, bi in zip(a, b)]
    for col in range(n):
        piv = next((r for r in range(col, n) if m[r][col] != 0), None)
        if piv is None:
            raise ValueError("singular matrix")
        m[col], m[piv] = m[piv], m[col]
        m[col] = [x / m[col][col] for x in m[col]]
        for r in range(n):
            if r != col and m[r][col] != 0:
                f = m[r][col]
                m[r] = [x - f * y for x, y in zip(m[r], m[col])]
    return [row[-1] for row in m]


if __name__ == "__main__":
    x = solve([[2, 1, -1], [-3, -1, 2], [-2, 1, 2]], [8, -11, -3])
    assert x == [2, 3, -1], x
    print("solution:", [str(v) for v in x])
