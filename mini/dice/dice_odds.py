"""Exact probability distribution of the sum of NdS dice (convolution)."""
import sys


def distribution(n: int, sides: int) -> dict[int, float]:
    dist = {0: 1.0}
    for _ in range(n):
        new: dict[int, float] = {}
        for total, p in dist.items():
            for face in range(1, sides + 1):
                new[total + face] = new.get(total + face, 0.0) + p / sides
        dist = new
    return dist


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 2
    sides = int(sys.argv[2]) if len(sys.argv) > 2 else 6
    d = distribution(n, sides)
    for total in sorted(d):
        print(f"{total:3} {d[total]:7.2%} {'#' * round(d[total] * 150)}")
    print("mean:", round(sum(t * p for t, p in d.items()), 3))
