"""Stochastic L-system: each rule has weighted alternatives; prints several seeded variants."""
import random
import sys

RULES = {"F": [(0.5, "F[+F]F[-F]F"), (0.3, "F[+F]F"), (0.2, "F[-F]F")]}


def expand_random(axiom: str, n: int, rng: random.Random) -> str:
    s = axiom
    for _ in range(n):
        out = []
        for c in s:
            opts = RULES.get(c)
            if opts:
                out.append(rng.choices([o[1] for o in opts], [o[0] for o in opts])[0])
            else:
                out.append(c)
        s = "".join(out)
    return s


if __name__ == "__main__":
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    for i in range(3):
        rng = random.Random(seed + i)
        s = expand_random("F", 3, rng)
        print(f"seed {seed + i}: len {len(s)}, branches {s.count('[')}")
