"""Solve a 0/1 knapsack with a genetic algorithm and check against dynamic programming."""
import random

WEIGHTS = [12, 7, 11, 8, 9, 6, 14, 5, 10, 13, 4, 3]
VALUES = [24, 13, 23, 15, 16, 11, 28, 8, 19, 25, 7, 5]
CAP = 40


def value(bits) -> int:
    w = sum(wt for b, wt in zip(bits, WEIGHTS) if b)
    return 0 if w > CAP else sum(v for b, v in zip(bits, VALUES) if b)


def dp_best() -> int:
    best = [0] * (CAP + 1)
    for w, v in zip(WEIGHTS, VALUES):
        for c in range(CAP, w - 1, -1):
            best[c] = max(best[c], best[c - w] + v)
    return best[CAP]


def main(seed: int = 3, gens: int = 60, size: int = 60) -> None:
    rng = random.Random(seed)
    n = len(WEIGHTS)
    pop = [[rng.random() < 0.3 for _ in range(n)] for _ in range(size)]
    for g in range(gens):
        pop.sort(key=value, reverse=True)
        elite = pop[: size // 4]
        pop = elite[:]
        while len(pop) < size:
            a, b = rng.sample(elite, 2)
            cut = rng.randrange(n)
            child = a[:cut] + b[cut:]
            child = [(not x) if rng.random() < 0.04 else x for x in child]
            pop.append(child)
    best = max(pop, key=value)
    print("GA best value:", value(best), "items:", [i for i, b in enumerate(best) if b])
    print("DP optimum:   ", dp_best())


if __name__ == "__main__":
    main()
