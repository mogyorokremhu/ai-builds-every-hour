"""LU decomposition (Doolittle, no pivoting) and linear solve, exact fractions."""
from fractions import Fraction


def lu(m: list[list]) -> tuple[list[list[Fraction]], list[list[Fraction]]]:
    """Return (L, U) with L unit lower triangular and A = L @ U."""
    n = len(m)
    a = [[Fraction(x) for x in row] for row in m]
    L = [[Fraction(int(i == j)) for j in range(n)] for i in range(n)]
    U = [[Fraction(0)] * n for _ in range(n)]
    for i in range(n):
        for k in range(i, n):
            U[i][k] = a[i][k] - sum(L[i][j] * U[j][k] for j in range(i))
        if U[i][i] == 0:
            raise ValueError("zero pivot; pivoting required")
        for k in range(i + 1, n):
            L[k][i] = (a[k][i] - sum(L[k][j] * U[j][i] for j in range(i))) / U[i][i]
    return L, U


def solve(m: list[list], b: list) -> list[Fraction]:
    """Solve m x = b via forward and back substitution."""
    L, U = lu(m)
    n = len(b)
    y = [Fraction(0)] * n
    for i in range(n):
        y[i] = Fraction(b[i]) - sum(L[i][j] * y[j] for j in range(i))
    x = [Fraction(0)] * n
    for i in reversed(range(n)):
        x[i] = (y[i] - sum(U[i][j] * x[j] for j in range(i + 1, n))) / U[i][i]
    return x


if __name__ == "__main__":
    A = [[2, 1, 1], [4, 3, 3], [8, 7, 9]]
    L, U = lu(A)
    prod = [[sum(L[i][k] * U[k][j] for k in range(3)) for j in range(3)] for i in range(3)]
    assert prod == [[Fraction(x) for x in r] for r in A]
    assert solve([[2, 1], [1, 3]], [3, 5]) == [Fraction(4, 5), Fraction(7, 5)]
    print("x =", [str(v) for v in solve([[2, 1], [1, 3]], [3, 5])])
    print("ok")
