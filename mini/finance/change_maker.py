"""Fewest coins/notes for an amount (dynamic programming). Usage: python change_maker.py [amount] [denoms...]"""
import sys


def make_change(amount: int, denoms: list[int]) -> list[int] | None:
    """Return a minimal list of denominations summing to amount, or None."""
    INF = float("inf")
    best = [0] + [INF] * amount
    pick = [0] * (amount + 1)
    for a in range(1, amount + 1):
        for d in denoms:
            if d <= a and best[a - d] + 1 < best[a]:
                best[a] = best[a - d] + 1
                pick[a] = d
    if best[amount] == INF:
        return None
    out = []
    while amount:
        out.append(pick[amount])
        amount -= pick[amount]
    return sorted(out, reverse=True)


def main(argv: list[str]) -> None:
    amount = int(argv[1]) if len(argv) > 1 else 1790
    denoms = [int(x) for x in argv[2:]] or [5, 10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000, 20000]
    res = make_change(amount, denoms)
    if res is None:
        print(f"Cannot make {amount} with {denoms}")
    else:
        print(f"{amount} = {' + '.join(map(str, res))}  ({len(res)} pieces)")


if __name__ == "__main__":
    main(sys.argv)
