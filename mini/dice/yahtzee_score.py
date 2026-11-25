"""Score a five-dice roll in every Yahtzee category."""
import random
from collections import Counter


def score(dice: list[int]) -> dict[str, int]:
    c = Counter(dice)
    counts = sorted(c.values(), reverse=True)
    total = sum(dice)
    s = set(dice)
    result = {name: n * c[n] for n, name in enumerate(
        ["ones", "twos", "threes", "fours", "fives", "sixes"], 1)}
    result["three of a kind"] = total if counts[0] >= 3 else 0
    result["four of a kind"] = total if counts[0] >= 4 else 0
    result["full house"] = 25 if counts == [3, 2] else 0
    result["small straight"] = 30 if any(set(r) <= s for r in
                                         ({1, 2, 3, 4}, {2, 3, 4, 5}, {3, 4, 5, 6})) else 0
    result["large straight"] = 40 if s in ({1, 2, 3, 4, 5}, {2, 3, 4, 5, 6}) else 0
    result["yahtzee"] = 50 if counts[0] == 5 else 0
    result["chance"] = total
    return result


if __name__ == "__main__":
    roll = sorted(random.randint(1, 6) for _ in range(5))
    print("Roll:", roll)
    for name, pts in score(roll).items():
        print(f"  {name:16}{pts:3}")
