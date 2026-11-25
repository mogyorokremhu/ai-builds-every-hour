"""Monty Hall problem: simulate staying vs. switching."""
import random


def play(switch: bool, rng: random.Random) -> bool:
    car, pick = rng.randrange(3), rng.randrange(3)
    opened = rng.choice([d for d in range(3) if d not in (car, pick)])
    if switch:
        pick = next(d for d in range(3) if d not in (pick, opened))
    return pick == car


def win_rate(switch: bool, trials: int = 30000, seed: int = 7) -> float:
    rng = random.Random(seed)
    return sum(play(switch, rng) for _ in range(trials)) / trials


if __name__ == "__main__":
    stay, swap = win_rate(False), win_rate(True)
    print(f"stay: {stay:.3f}  switch: {swap:.3f}")
    assert abs(stay - 1 / 3) < 0.02 and abs(swap - 2 / 3) < 0.02
    print("ok")
