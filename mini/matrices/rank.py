"""Matrix rank and reduced row echelon form with exact fractions."""
from fractions import Fraction


def rref(m: list[list]) -> tuple[list[list[Fraction]], list[int]]:
    """Return (RREF matrix, pivot column indices)."""
    a = [[Fraction(x) for x in row] for row in m]
    rows, cols = len(a), len(a[0]) if a else 0
    pivots: list[int] = []
    r = 0
    for c in range(cols):
        if r >= rows:
            break
        p = next((i for i in range(r, rows) if a[i][c] != 0), None)
        if p is None:
            continue
        a[r], a[p] = a[p], a[r]
        a[r] = [x / a[r][c] for x in a[r]]
        for i in range(rows):
            if i != r and a[i][c] != 0:
                f = a[i][c]
                a[i] = [x - f * y for x, y in zip(a[i], a[r])]
        pivots.append(c)
        r += 1
    return a, pivots


def rank(m: list[list]) -> int:
    """Rank of a matrix."""
    return len(rref(m)[1])


if __name__ == "__main__":
    assert rank([[1, 2], [3, 4]]) == 2
    assert rank([[1, 2, 3], [2, 4, 6], [1, 0, 1]]) == 2
    assert rank([[0, 0], [0, 0]]) == 0
    assert rref([[1, 2, 3], [4, 5, 6]])[0][0] == [1, 0, -1]
    print("rank([[1,2,3],[2,4,6],[1,0,1]]) =", rank([[1, 2, 3], [2, 4, 6], [1, 0, 1]]))
    print("ok")
