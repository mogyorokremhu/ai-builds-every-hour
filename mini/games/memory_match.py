"""Memory (concentration) card game: a perfect-memory AI vs. a forgetful one. `python memory_match.py [seed]`."""
import random
import sys


def play(rng: random.Random, memory: float, pairs: int = 12) -> int:
    """Solo game: return the number of turns to clear the board; `memory` = chance of recalling a seen card."""
    cards = list(range(pairs)) * 2
    rng.shuffle(cards)
    left = set(range(len(cards)))
    known: dict[int, int] = {}
    turns = 0
    while left:
        turns += 1
        unseen = [i for i in left if i not in known]
        a = rng.choice(unseen or sorted(left))
        known[a] = cards[a]
        match = next((j for j in left if j != a and j in known and known[j] == cards[a]
                      and rng.random() < memory), None)
        if match is None:
            rest = [i for i in left if i != a and i not in known] or [i for i in left if i != a]
            b = rng.choice(rest)
            known[b] = cards[b]
        else:
            b = match
        if cards[a] == cards[b]:
            left -= {a, b}
            known.pop(a, None)
            known.pop(b, None)
    return turns


def main() -> None:
    rng = random.Random(int(sys.argv[1]) if len(sys.argv) > 1 else 1)
    for m in (0.0, 0.5, 0.9, 1.0):
        t = [play(rng, m) for _ in range(300)]
        print(f"memory {m:.1f}: avg {sum(t)/len(t):5.1f} turns (best {min(t)}, worst {max(t)})")


if __name__ == "__main__":
    main()
