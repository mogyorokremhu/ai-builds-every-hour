"""Base-rate fallacy: exact Bayes posterior vs. a simulated screening population."""
import random


def posterior(prevalence: float, sensitivity: float, specificity: float) -> float:
    tp = prevalence * sensitivity
    fp = (1 - prevalence) * (1 - specificity)
    return tp / (tp + fp)


def simulate(prevalence: float, sensitivity: float, specificity: float,
             people: int = 400000, seed: int = 11) -> float:
    rng = random.Random(seed)
    pos = true_pos = 0
    for _ in range(people):
        sick = rng.random() < prevalence
        positive = rng.random() < (sensitivity if sick else 1 - specificity)
        if positive:
            pos += 1
            true_pos += sick
    return true_pos / pos


if __name__ == "__main__":
    exact = posterior(0.01, 0.95, 0.95)
    sim = simulate(0.01, 0.95, 0.95)
    print(f"P(sick | positive): exact {exact:.3f}, simulated {sim:.3f}")
    assert abs(exact - 0.161) < 0.001 and abs(sim - exact) < 0.02
    print("ok")
