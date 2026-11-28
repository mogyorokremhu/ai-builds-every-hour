"""Evolve a random string toward a target with a simple genetic algorithm."""
import random
import string

TARGET = "hello evolution"
ALPHABET = string.ascii_lowercase + " "


def fitness(s: str) -> int:
    return sum(a == b for a, b in zip(s, TARGET))


def evolve(pop_size: int = 100, mutation: float = 0.05, seed: int = 1) -> int:
    rng = random.Random(seed)
    pop = ["".join(rng.choice(ALPHABET) for _ in TARGET) for _ in range(pop_size)]
    gen = 0
    while True:
        pop.sort(key=fitness, reverse=True)
        if gen % 10 == 0 or pop[0] == TARGET:
            print(f"gen {gen:3d}: {pop[0]!r} fitness={fitness(pop[0])}")
        if pop[0] == TARGET:
            return gen
        parents = pop[: pop_size // 5]
        children = []
        while len(children) < pop_size:
            a, b = rng.sample(parents, 2)
            cut = rng.randrange(len(TARGET))
            child = [c if rng.random() > mutation else rng.choice(ALPHABET) for c in a[:cut] + b[cut:]]
            children.append("".join(child))
        pop = children
        gen += 1


if __name__ == "__main__":
    evolve()
