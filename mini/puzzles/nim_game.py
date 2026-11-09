"""Nim solver: nim-sum strategy, verified against brute-force minimax on small piles."""
from functools import lru_cache
from functools import reduce
from operator import xor


def nim_sum(piles) -> int:
    return reduce(xor, piles, 0)


def winning_move(piles):
    """Return (pile index, new size) that leaves nim-sum 0, or None if losing."""
    s = nim_sum(piles)
    if s == 0:
        return None
    for i, p in enumerate(piles):
        if p ^ s < p:
            return i, p ^ s


@lru_cache(maxsize=None)
def brute_wins(piles: tuple) -> bool:
    """True if the player to move wins (normal play)."""
    for i, p in enumerate(piles):
        for k in range(p):
            nxt = tuple(sorted(piles[:i] + (k,) + piles[i + 1:]))
            if not brute_wins(nxt):
                return True
    return False


if __name__ == "__main__":
    import itertools
    for piles in itertools.product(range(5), repeat=3):
        assert (winning_move(piles) is not None) == brute_wins(tuple(sorted(piles))), piles
    print("nim-sum strategy matches minimax for all piles up to 4x3")
    print("piles 3,4,5 ->", winning_move((3, 4, 5)))
