"""Ackermann function with memoisation, plus a call counter to show its explosive growth."""
import sys
from functools import lru_cache

sys.setrecursionlimit(100000)
calls = 0


@lru_cache(maxsize=None)
def ack(m: int, n: int) -> int:
    """Ackermann-Peter function."""
    global calls
    calls += 1
    if m == 0:
        return n + 1
    if n == 0:
        return ack(m - 1, 1)
    return ack(m - 1, ack(m, n - 1))


if __name__ == "__main__":
    for m in range(4):
        print(m, [ack(m, n) for n in range(5)])
    assert ack(2, 3) == 9 and ack(3, 3) == 61
    print("distinct calls computed:", calls)
