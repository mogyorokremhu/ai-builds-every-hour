"""Chinese Remainder Theorem solver (python chinese_remainder.py 2:3 3:5 2:7)."""
import sys


def egcd(a: int, b: int) -> tuple[int, int, int]:
    """Extended Euclid: returns (g, x, y) with a*x + b*y = g."""
    if b == 0:
        return a, 1, 0
    g, x, y = egcd(b, a % b)
    return g, y, x - (a // b) * y


def crt(congruences: list[tuple[int, int]]) -> tuple[int, int] | None:
    """Solve x = r_i (mod m_i) for possibly non-coprime moduli; returns (x, lcm) or None."""
    x, m = 0, 1
    for r, mod in congruences:
        g, p, _ = egcd(m, mod)
        if (r - x) % g:
            return None
        lcm = m // g * mod
        x = (x + m * ((r - x) // g * p % (mod // g))) % lcm
        m = lcm
    return x, m


if __name__ == "__main__":
    args = sys.argv[1:] or ["2:3", "3:5", "2:7"]
    pairs = [tuple(map(int, a.split(":"))) for a in args]
    res = crt(pairs)
    print("no solution" if res is None else f"x = {res[0]} (mod {res[1]})")
