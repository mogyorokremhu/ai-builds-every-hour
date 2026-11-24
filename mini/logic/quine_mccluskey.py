"""Quine-McCluskey boolean minimizer: minterms -> minimal sum-of-products."""
from itertools import combinations


def prime_implicants(minterms: list[int], nbits: int) -> set[str]:
    terms = {format(m, f"0{nbits}b") for m in minterms}
    primes: set[str] = set()
    while terms:
        used: set[str] = set()
        nxt: set[str] = set()
        for a, b in combinations(sorted(terms), 2):
            diff = [i for i in range(nbits) if a[i] != b[i]]
            if len(diff) == 1:
                i = diff[0]
                nxt.add(a[:i] + "-" + a[i + 1:])
                used |= {a, b}
        primes |= terms - used
        terms = nxt
    return primes


def covers(p: str, m: int) -> bool:
    bits = format(m, f"0{len(p)}b")
    return all(x == "-" or x == y for x, y in zip(p, bits))


def minimize(minterms: list[int], nbits: int) -> list[str]:
    primes = sorted(prime_implicants(minterms, nbits))
    for k in range(1, len(primes) + 1):  # smallest cover by brute force
        for combo in combinations(primes, k):
            if all(any(covers(p, m) for p in combo) for m in minterms):
                return list(combo)
    return []


def to_expr(implicants: list[str], names: str = "ABCD") -> str:
    out = []
    for p in implicants:
        t = "".join(names[i] + ("" if c == "1" else "'") for i, c in enumerate(p) if c != "-")
        out.append(t or "1")
    return " + ".join(out) or "0"


if __name__ == "__main__":
    sol = minimize([0, 1, 2, 5, 6, 7], 3)
    print(to_expr(sol, "ABC"))
    assert all(any(covers(p, m) for p in sol) for m in [0, 1, 2, 5, 6, 7])
    assert not any(covers(p, m) for p in sol for m in (3, 4))
    print("ok")
