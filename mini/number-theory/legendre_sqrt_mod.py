"""Legendre symbol and Tonelli-Shanks square roots modulo a prime."""
import sys


def legendre(a: int, p: int) -> int:
    """Return 1 if a is a QR mod odd prime p, -1 if not, 0 if p | a."""
    r = pow(a % p, (p - 1) // 2, p)
    return -1 if r == p - 1 else r


def tonelli_shanks(n: int, p: int):
    """Return x with x*x = n (mod p), or None if none exists."""
    n %= p
    if n == 0:
        return 0
    if legendre(n, p) != 1:
        return None
    q, s = p - 1, 0
    while q % 2 == 0:
        q //= 2
        s += 1
    z = 2
    while legendre(z, p) != -1:
        z += 1
    m, c, t, r = s, pow(z, q, p), pow(n, q, p), pow(n, (q + 1) // 2, p)
    while t != 1:
        i, tt = 0, t
        while tt != 1:
            tt = tt * tt % p
            i += 1
        b = pow(c, 1 << (m - i - 1), p)
        m, c, t, r = i, b * b % p, t * b * b % p, r * b % p
    return r


if __name__ == "__main__":
    n, p = (int(sys.argv[1]), int(sys.argv[2])) if len(sys.argv) > 2 else (10, 13)
    r = tonelli_shanks(n, p)
    print(f"legendre({n}/{p}) = {legendre(n, p)}")
    print("no square root" if r is None else f"sqrt({n}) mod {p} = {r} and {p - r}")
