"""Simulate coin flips and report the longest run and run-length counts."""
import random
import sys
from collections import Counter


def flips(n: int, rng: random.Random) -> str:
    """Return a string of n flips, H or T."""
    return "".join(rng.choice("HT") for _ in range(n))


def runs(s: str) -> list[int]:
    """Lengths of maximal runs of equal characters."""
    out: list[int] = []
    prev = ""
    for ch in s:
        if ch == prev:
            out[-1] += 1
        else:
            out.append(1)
            prev = ch
    return out


def main() -> None:
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 100
    seed = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    s = flips(n, random.Random(seed))
    r = runs(s)
    print(s)
    print(f"flips={n} runs={len(r)} longest={max(r)}")
    for length, count in sorted(Counter(r).items()):
        print(f"  run of {length}: {count} {'#' * count}")


if __name__ == "__main__":
    main()
