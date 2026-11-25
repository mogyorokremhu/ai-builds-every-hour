"""Penrose-style Robinson triangle subdivision: counts triangles per generation and
checks that the thick/thin ratio converges to the golden ratio."""
from math import sqrt

PHI = (1 + sqrt(5)) / 2


def subdivide(counts: tuple[int, int]) -> tuple[int, int]:
    """One deflation step on (thin, thick) triangle counts.

    thin -> 1 thin + 1 thick ; thick -> 2 thick + 1 thin  (Robinson triangles)."""
    thin, thick = counts
    return thin + thick, thin + 2 * thick


def main() -> None:
    counts = (1, 0)
    for gen in range(1, 16):
        counts = subdivide(counts)
        ratio = counts[1] / counts[0]
        print(f"gen {gen:2}: thin={counts[0]:6} thick={counts[1]:6} ratio={ratio:.6f}")
    assert abs(counts[1] / counts[0] - PHI) < 1e-3
    print(f"golden ratio = {PHI:.6f}  (check passed)")


if __name__ == "__main__":
    main()
