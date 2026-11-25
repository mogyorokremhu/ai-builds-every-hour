"""Gambler's ruin: simulated vs. exact ruin probability for a fair/unfair coin."""
import random


def exact_ruin(start: int, goal: int, p: float) -> float:
    """Probability of hitting 0 before `goal`, winning each bet with probability p."""
    if p == 0.5:
        return 1 - start / goal
    r = (1 - p) / p
    return (r**start - r**goal) / (1 - r**goal)


def simulate(start: int, goal: int, p: float, trials: int = 10000, seed: int = 3) -> float:
    rng = random.Random(seed)
    ruined = 0
    for _ in range(trials):
        money = start
        while 0 < money < goal:
            money += 1 if rng.random() < p else -1
        ruined += money == 0
    return ruined / trials


if __name__ == "__main__":
    for p in (0.5, 0.48, 0.55):
        print(f"p={p}: exact={exact_ruin(10, 20, p):.4f} simulated={simulate(10, 20, p):.4f}")
    assert abs(simulate(10, 20, 0.5) - 0.5) < 0.03
    print("ok")
