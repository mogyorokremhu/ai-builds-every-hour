#!/usr/bin/env python3
"""Primes: `primes_cli.py 30` lists primes <= 30, `-f N` factorises N."""
import sys


def sieve(n):
    if n < 2:
        return []
    s = bytearray([1]) * (n + 1)
    s[0] = s[1] = 0
    for i in range(2, int(n ** 0.5) + 1):
        if s[i]:
            s[i * i::i] = bytearray(len(s[i * i::i]))
    return [i for i, v in enumerate(s) if v]


def factorize(n):
    out, d = {}, 2
    while d * d <= n:
        while n % d == 0:
            out[d] = out.get(d, 0) + 1
            n //= d
        d += 1
    if n > 1:
        out[n] = out.get(n, 0) + 1
    return out


if __name__ == "__main__":
    a = sys.argv[1:]
    if a == ["--selftest"]:
        assert sieve(20) == [2, 3, 5, 7, 11, 13, 17, 19]
        assert factorize(360) == {2: 3, 3: 2, 5: 1}
        print("ok")
    elif a[:1] == ["-f"]:
        f = factorize(int(a[1]))
        print(" * ".join(f"{p}^{e}" if e > 1 else str(p) for p, e in f.items()))
    else:
        print(*sieve(int(a[0])))
