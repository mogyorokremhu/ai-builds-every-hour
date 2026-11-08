#!/usr/bin/env python3
"""nim - optimal Nim play via XOR (nim-sum), plus Sprague-Grundy values for subtraction games.

  python3 nim.py 3 4 5            best move for piles 3,4,5
  python3 nim.py --play 3 4 5     play against the perfect opponent (you move first)
  python3 nim.py --grundy 1,3,4 10   Grundy values 0..10 for a subtraction game {1,3,4}
"""
import sys
from functools import reduce


def nim_sum(piles):
    return reduce(lambda a, b: a ^ b, piles, 0)


def best_move(piles):
    """Return (pile_index, new_size) that leaves nim-sum 0, or None if already lost."""
    s = nim_sum(piles)
    if s == 0:
        return None
    for i, p in enumerate(piles):
        if p ^ s < p:
            return i, p ^ s


def grundy(moves, n):
    g = []
    for k in range(n + 1):
        reach = {g[k - m] for m in moves if k - m >= 0}
        v = 0
        while v in reach:
            v += 1
        g.append(v)
    return g


def play(piles):
    piles = list(piles)
    while any(piles):
        print("piles:", piles)
        try:
            i, n = map(int, input("take n from pile i (i n): ").split())
            assert 0 <= i < len(piles) and 1 <= n <= piles[i]
        except (ValueError, AssertionError):
            print("invalid"); continue
        piles[i] -= n
        if not any(piles):
            print("You took the last object - you win!"); return
        mv = best_move(piles) or next((j, piles[j] - 1) for j in range(len(piles)) if piles[j])
        print(f"I take {piles[mv[0]] - mv[1]} from pile {mv[0]}")
        piles[mv[0]] = mv[1]
    print("I took the last object - I win!")


def selftest():
    assert nim_sum([3, 4, 5]) == 2
    assert best_move([1, 2, 3]) is None
    i, n = best_move([3, 4, 5]); p = [3, 4, 5]; p[i] = n
    assert nim_sum(p) == 0
    assert grundy([1, 2, 3], 8) == [0, 1, 2, 3, 0, 1, 2, 3, 0]
    print("ok")


if __name__ == "__main__":
    a = sys.argv[1:]
    if not a or a[0] == "--selftest": selftest()
    elif a[0] == "--play": play(map(int, a[1:]))
    elif a[0] == "--grundy": print(*grundy([int(x) for x in a[1].split(",")], int(a[2])))
    else:
        p = list(map(int, a)); m = best_move(p)
        print("lost position (nim-sum 0)" if m is None else f"take {p[m[0]] - m[1]} from pile {m[0]} -> {m[1]} left")
