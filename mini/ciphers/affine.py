"""Affine cipher: E(x) = (a*x + b) mod 26. Usage: python affine.py [-d] a b "text" """
import sys
from math import gcd


def affine(s: str, a: int, b: int, decrypt: bool = False) -> str:
    if gcd(a, 26) != 1:
        raise ValueError("a must be coprime with 26")
    inv = pow(a, -1, 26)
    out = []
    for c in s:
        if c.isascii() and c.isalpha():
            base = ord("A") if c.isupper() else ord("a")
            x = ord(c) - base
            y = inv * (x - b) % 26 if decrypt else (a * x + b) % 26
            out.append(chr(base + y))
        else:
            out.append(c)
    return "".join(out)


if __name__ == "__main__":
    args = sys.argv[1:]
    dec = "-d" in args
    args = [x for x in args if x != "-d"]
    a, b = (int(args[0]), int(args[1])) if len(args) >= 2 else (5, 8)
    text = " ".join(args[2:]) or "Affine Cipher"
    res = affine(text, a, b, dec)
    print(res)
    assert affine(res, a, b, not dec) == text
