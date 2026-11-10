"""Coin change: fewest coins and number of ways to make an amount (DP).

Usage: python coin_change.py [amount] [coin ...]
"""
import sys


def fewest(coins: list[int], amount: int) -> list[int] | None:
    inf = float("inf")
    best = [0] + [inf] * amount
    pick = [0] * (amount + 1)
    for a in range(1, amount + 1):
        for c in coins:
            if c <= a and best[a - c] + 1 < best[a]:
                best[a] = best[a - c] + 1
                pick[a] = c
    if best[amount] == inf:
        return None
    out = []
    while amount:
        out.append(pick[amount])
        amount -= pick[amount]
    return out


def ways(coins: list[int], amount: int) -> int:
    w = [1] + [0] * amount
    for c in coins:
        for a in range(c, amount + 1):
            w[a] += w[a - c]
    return w[amount]


if __name__ == "__main__":
    amount = int(sys.argv[1]) if len(sys.argv) > 1 else 63
    coins = [int(a) for a in sys.argv[2:]] or [1, 5, 10, 21, 25]
    print("coins:", coins, "amount:", amount)
    print("fewest:", fewest(coins, amount))
    print("ways:", ways(coins, amount))
