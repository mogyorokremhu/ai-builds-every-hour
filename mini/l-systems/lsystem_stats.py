"""Print growth statistics (length, symbol counts, growth ratio) for L-systems."""
import sys
from collections import Counter

from expand import SYSTEMS, expand


def stats(name: str, gens: int) -> None:
    axiom, rules = SYSTEMS[name]
    prev = len(axiom)
    print(f"== {name} ==")
    for g in range(gens + 1):
        s = expand(axiom, rules, g)
        ratio = len(s) / prev if prev else 0
        top = ", ".join(f"{k}:{v}" for k, v in Counter(s).most_common(4))
        print(f"gen {g}: len {len(s):>7}  x{ratio:5.2f}  {top}")
        prev = len(s)


if __name__ == "__main__":
    names = sys.argv[1:] or list(SYSTEMS)
    for n in names:
        stats(n, 6)
