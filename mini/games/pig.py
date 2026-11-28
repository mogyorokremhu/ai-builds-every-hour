"""Pig dice game: hold-at-N strategies play each other. `python pig.py [seed]` prints a win-rate table."""
import random
import sys


def turn(rng: random.Random, hold: int) -> int:
    """Roll until the turn total reaches `hold` (bank it) or a 1 is rolled (score 0)."""
    total = 0
    while total < hold:
        d = rng.randint(1, 6)
        if d == 1:
            return 0
        total += d
    return total


def game(rng: random.Random, h1: int, h2: int, goal: int = 100) -> int:
    """Return 0 if player 1 wins, 1 otherwise. Player 1 moves first."""
    s = [0, 0]
    holds = (h1, h2)
    p = 0
    while True:
        h = min(holds[p], goal - s[p])
        s[p] += turn(rng, h)
        if s[p] >= goal:
            return p
        p ^= 1


def main() -> None:
    rng = random.Random(int(sys.argv[1]) if len(sys.argv) > 1 else 1)
    holds = (10, 15, 20, 25, 30)
    n = 400
    print("hold " + "".join(f"{h:>6}" for h in holds))
    for a in holds:
        row = []
        for b in holds:
            w = sum(game(rng, a, b) == 0 for _ in range(n))
            row.append(f"{100 * w // n:>5}%")
        print(f"{a:>4} " + "".join(row))


if __name__ == "__main__":
    main()
