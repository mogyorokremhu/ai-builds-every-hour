"""Modular arithmetic: extended gcd, inverse, CRT, fast pow, with self-checks."""


def egcd(a: int, b: int) -> tuple[int, int, int]:
    """Return (g, x, y) with a*x + b*y == g == gcd(a, b)."""
    if b == 0:
        return a, 1, 0
    g, x, y = egcd(b, a % b)
    return g, y, x - (a // b) * y


def modinv(a: int, m: int) -> int:
    """Modular inverse of a mod m; raises ValueError if none exists."""
    g, x, _ = egcd(a % m, m)
    if g != 1:
        raise ValueError(f"{a} has no inverse mod {m}")
    return x % m


def crt(residues: list[int], moduli: list[int]) -> int:
    """Chinese remainder theorem for pairwise coprime moduli."""
    M = 1
    for m in moduli:
        M *= m
    total = 0
    for r, m in zip(residues, moduli):
        Mi = M // m
        total += r * Mi * modinv(Mi, m)
    return total % M


if __name__ == "__main__":
    assert (3 * modinv(3, 11)) % 11 == 1
    assert crt([2, 3, 2], [3, 5, 7]) == 23
    assert pow(7, 128, 13) == 3
    print("inverse of 3 mod 11 =", modinv(3, 11))
    print("x = 2 (3), 3 (5), 2 (7) ->", crt([2, 3, 2], [3, 5, 7]))
