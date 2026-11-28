"""Blackjack with basic-strategy-lite vs. a dealer-mimic player. `python blackjack_basic.py [seed]` simulates 20000 hands."""
import random
import sys


def value(hand: list[int]) -> tuple[int, bool]:
    """Best total and whether it is soft."""
    t = sum(hand)
    if 1 in hand and t + 10 <= 21:
        return t + 10, True
    return t, False


def draw(rng: random.Random) -> int:
    return min(rng.randint(1, 13), 10)


def player_hits(hand: list[int], up: int) -> bool:
    t, soft = value(hand)
    if soft:
        return t < 18 or (t == 18 and up >= 9)
    if t >= 17:
        return False
    if t >= 13:
        return up >= 7
    if t == 12:
        return not 4 <= up <= 6
    return True


def play(rng: random.Random, strategy: str) -> int:
    """Return +1 win, 0 push, -1 loss for one hand."""
    p, d = [draw(rng), draw(rng)], [draw(rng), draw(rng)]
    if value(p)[0] == 21:
        return 0 if value(d)[0] == 21 else 1
    while (player_hits(p, d[0]) if strategy == "basic" else value(p)[0] < 17):
        p.append(draw(rng))
        if value(p)[0] > 21:
            return -1
    while value(d)[0] < 17:
        d.append(draw(rng))
    pt, dt = value(p)[0], value(d)[0]
    if dt > 21 or pt > dt:
        return 1
    return 0 if pt == dt else -1


def main() -> None:
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    for strategy in ("mimic", "basic"):
        rng = random.Random(seed)
        n = 20000
        r = [play(rng, strategy) for _ in range(n)]
        print(f"{strategy:>6}: win {r.count(1)/n:.1%} push {r.count(0)/n:.1%} loss {r.count(-1)/n:.1%} edge {sum(r)/n:+.3f}")


if __name__ == "__main__":
    main()
