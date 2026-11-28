"""Shorten a random tour of cities with 2-opt hill climbing and random restarts."""
import math
import random


def tour_length(pts, tour) -> float:
    return sum(math.dist(pts[tour[i]], pts[tour[(i + 1) % len(tour)]]) for i in range(len(tour)))


def two_opt(pts, tour):
    improved = True
    while improved:
        improved = False
        for i in range(1, len(tour) - 1):
            for j in range(i + 1, len(tour)):
                new = tour[:i] + tour[i:j + 1][::-1] + tour[j + 1:]
                if tour_length(pts, new) < tour_length(pts, tour) - 1e-9:
                    tour, improved = new, True
    return tour


def main(n: int = 25, restarts: int = 5, seed: int = 7) -> None:
    rng = random.Random(seed)
    pts = [(rng.random() * 100, rng.random() * 100) for _ in range(n)]
    best = None
    for r in range(restarts):
        tour = list(range(n))
        rng.shuffle(tour)
        start = tour_length(pts, tour)
        tour = two_opt(pts, tour)
        length = tour_length(pts, tour)
        print(f"restart {r}: {start:7.1f} -> {length:7.1f}")
        if best is None or length < best[0]:
            best = (length, tour)
    print(f"best tour length {best[0]:.1f}: {best[1]}")


if __name__ == "__main__":
    main()
