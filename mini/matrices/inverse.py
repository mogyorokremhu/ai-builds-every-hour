"""Matrix inverse by Gauss-Jordan elimination with exact fractions."""
from fractions import Fraction


def inverse(m: list[list]) -> list[list[Fraction]]:
    """Return the inverse of a square matrix; raises ValueError if singular."""
    n = len(m)
    a = [[Fraction(x) for x in row] + [Fraction(int(i == j)) for j in range(n)]
         for i, row in enumerate(m)]
    for c in range(n):
        p = next((r for r in range(c, n) if a[r][c] != 0), None)
        if p is None:
            raise ValueError("singular matrix")
        a[c], a[p] = a[p], a[c]
        pv = a[c][c]
        a[c] = [x / pv for x in a[c]]
        for r in range(n):
            if r != c and a[r][c] != 0:
                f = a[r][c]
                a[r] = [x - f * y for x, y in zip(a[r], a[c])]
    return [row[n:] for row in a]


def matmul(a, b):
    return [[sum(x * y for x, y in zip(r, c)) for c in zip(*b)] for r in a]


if __name__ == "__main__":
    m = [[2, 1, 1], [1, 3, 2], [1, 0, 0]]
    inv = inverse(m)
    ident = matmul(m, inv)
    assert all(ident[i][j] == int(i == j) for i in range(3) for j in range(3))
    try:
        inverse([[1, 2], [2, 4]])
        raise SystemExit("should fail")
    except ValueError:
        pass
    for row in inv:
        print([str(x) for x in row])
    print("ok")
