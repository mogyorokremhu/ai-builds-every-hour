"""Compare the rule of 72 with the exact doubling time."""
import math


def exact_doubling(rate_pct: float) -> float:
    return math.log(2) / math.log(1 + rate_pct / 100)


if __name__ == "__main__":
    print("rate%  rule72  exact   error")
    for r in (1, 2, 4, 6, 8, 12, 18, 24):
        approx = 72 / r
        ex = exact_doubling(r)
        print(f"{r:>5}  {approx:6.2f}  {ex:6.2f}  {approx - ex:+.2f}")
