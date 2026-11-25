"""Check boolean-law identities (De Morgan, absorption, ...) by exhaustive evaluation."""
from itertools import product

LAWS = {
    "De Morgan 1": (lambda a, b: not (a and b), lambda a, b: (not a) or (not b)),
    "De Morgan 2": (lambda a, b: not (a or b), lambda a, b: (not a) and (not b)),
    "Absorption": (lambda a, b: a or (a and b), lambda a, b: a),
    "Implication": (lambda a, b: (not a) or b, lambda a, b: (not b) <= (not a)),
    "XOR": (lambda a, b: a != b, lambda a, b: (a or b) and not (a and b)),
}


def equivalent(f, g) -> bool:
    return all(bool(f(a, b)) == bool(g(a, b)) for a, b in product([False, True], repeat=2))


if __name__ == "__main__":
    for name, (f, g) in LAWS.items():
        print(f"{name:12} {'holds' if equivalent(f, g) else 'FAILS'}")
        assert equivalent(f, g)
    print("ok")
