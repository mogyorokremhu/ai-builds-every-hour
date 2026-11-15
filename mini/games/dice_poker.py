"""Dice poker: five dice, one reroll, score the hand. `--auto` plays 1000 rounds with a keep-pairs strategy."""
import random
import sys
from collections import Counter


def score(dice):
    c = sorted(Counter(dice).values(), reverse=True)
    if c[0] == 5:
        return "five of a kind", 50
    if c[0] == 4:
        return "four of a kind", 30
    if c[:2] == [3, 2]:
        return "full house", 25
    if sorted(dice) in ([1, 2, 3, 4, 5], [2, 3, 4, 5, 6]):
        return "straight", 20
    if c[0] == 3:
        return "three of a kind", 10
    if c[:2] == [2, 2]:
        return "two pair", 5
    if c[0] == 2:
        return "pair", 2
    return "nothing", 0


def auto_keep(dice):
    cnt = Counter(dice)
    best = max(cnt.values())
    if best == 1:
        return [i for i, d in enumerate(dice) if d == max(dice)][:1]
    return [i for i, d in enumerate(dice) if cnt[d] >= 2]


def play(rng, keep_fn):
    dice = [rng.randint(1, 6) for _ in range(5)]
    keep = set(keep_fn(dice))
    dice = [d if i in keep else rng.randint(1, 6) for i, d in enumerate(dice)]
    return dice, score(dice)


def main():
    rng = random.Random(7 if "--auto" in sys.argv else None)
    if "--auto" in sys.argv:
        total = 0
        names = Counter()
        for _ in range(1000):
            _, (n, p) = play(rng, auto_keep)
            total += p
            names[n] += 1
        print("average score:", total / 1000)
        for n, k in names.most_common():
            print(f"  {n:16}{k}")
        return
    dice = [rng.randint(1, 6) for _ in range(5)]
    print("Dice:", dice)
    ans = input("Positions to keep (e.g. 1 3 4), blank rerolls all: ").split()
    keep = {int(a) - 1 for a in ans if a.isdigit() and 1 <= int(a) <= 5}
    dice = [d if i in keep else rng.randint(1, 6) for i, d in enumerate(dice)]
    n, p = score(dice)
    print("Final:", dice, "->", n, f"({p} points)")


if __name__ == "__main__":
    main()
