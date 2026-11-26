"""Counting domino tilings of a 2 x n board (Fibonacci) and an m x n board (transfer by DP)."""
from functools import lru_cache


def tilings_2xn(n: int) -> int:
    a, b = 1, 1
    for _ in range(n):
        a, b = b, a + b
    return a


def domino_tilings(m: int, n: int) -> int:
    """Number of domino tilings of an m x n board using row-by-row bitmask DP."""
    if (m * n) % 2:
        return 0

    @lru_cache(maxsize=None)
    def go(row: int, mask: int) -> int:
        if row == m:
            return 1 if mask == 0 else 0
        total = 0

        def fill(col: int, cur: int, nxt: int) -> None:
            nonlocal total
            if col == n:
                total += go(row + 1, nxt)
                return
            if cur >> col & 1:
                fill(col + 1, cur, nxt)
                return
            fill(col + 1, cur, nxt | 1 << col)  # vertical domino
            if col + 1 < n and not cur >> (col + 1) & 1:
                fill(col + 2, cur, nxt)  # horizontal domino

        fill(0, mask, 0)
        return total

    return go(0, 0)


if __name__ == "__main__":
    assert [tilings_2xn(k) for k in range(1, 7)] == [1, 2, 3, 5, 8, 13]
    assert domino_tilings(2, 3) == 3 and domino_tilings(3, 3) == 0
    assert domino_tilings(4, 4) == 36 and domino_tilings(8, 8) == 12988816
    print("8x8 chessboard domino tilings:", domino_tilings(8, 8))
