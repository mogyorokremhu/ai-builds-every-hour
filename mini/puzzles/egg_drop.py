"""Egg drop puzzle: fewest drops in the worst case with e eggs and f floors.

Usage: python egg_drop.py [eggs] [floors]     (default: 2 eggs, 100 floors)
"""
import sys


def min_drops(eggs: int, floors: int) -> int:
    """Smallest t such that eggs eggs and t drops can cover `floors` floors."""
    reach = [0] * (eggs + 1)  # reach[e] = floors coverable with e eggs
    t = 0
    while reach[eggs] < floors:
        t += 1
        for e in range(eggs, 0, -1):
            reach[e] = reach[e] + reach[e - 1] + 1
    return t


def brute(eggs: int, floors: int) -> int:
    memo: dict[tuple[int, int], int] = {}

    def f(e: int, n: int) -> int:
        if n == 0 or e == 1 or n == 1:
            return n if e > 1 or n <= 1 else n
        if (e, n) not in memo:
            memo[(e, n)] = 1 + min(max(f(e - 1, k - 1), f(e, n - k)) for k in range(1, n + 1))
        return memo[(e, n)]

    return f(eggs, floors)


if __name__ == "__main__":
    e = int(sys.argv[1]) if len(sys.argv) > 1 else 2
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 100
    print(f"{e} eggs, {n} floors -> {min_drops(e, n)} drops")
    for ee in (1, 2, 3):
        for nn in (1, 5, 10, 20):
            assert min_drops(ee, nn) == brute(ee, nn), (ee, nn)
    print("matches brute-force DP on small cases")
