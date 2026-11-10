#!/usr/bin/env python3
"""fizzlist - generalized FizzBuzz: `fizzlist.py 20 3=Fizz 5=Buzz 7=Bazz`. `--selftest` runs checks."""
import sys

def fizz(n: int, rules: list[tuple[int, str]]) -> list[str]:
    return ["".join(w for d, w in rules if i % d == 0) or str(i) for i in range(1, n + 1)]

if __name__ == "__main__":
    if "--selftest" in sys.argv:
        assert fizz(15, [(3, "Fizz"), (5, "Buzz")])[-1] == "FizzBuzz" and fizz(2, [(3, "F")]) == ["1", "2"]; print("ok"); sys.exit()
    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    n = int(args[0]) if args else 30
    rules = [(int(a.split("=")[0]), a.split("=")[1]) for a in args[1:]] or [(3, "Fizz"), (5, "Buzz")]
    print("\n".join(fizz(n, rules)))
