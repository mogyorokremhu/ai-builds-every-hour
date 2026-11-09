"""Rail fence transposition cipher: python rail_fence.py enc 3 "WEAREDISCOVERED" """
import sys


def _pattern(n: int, rails: int) -> list[int]:
    if rails < 2:
        return [0] * n
    cyc = list(range(rails)) + list(range(rails - 2, 0, -1))
    return [cyc[i % len(cyc)] for i in range(n)]


def encrypt(text: str, rails: int) -> str:
    p = _pattern(len(text), rails)
    return "".join(c for r in range(rails) for c, q in zip(text, p) if q == r)


def decrypt(text: str, rails: int) -> str:
    p = _pattern(len(text), rails)
    order = sorted(range(len(text)), key=lambda i: (p[i], i))
    out = [""] * len(text)
    for ch, i in zip(text, order):
        out[i] = ch
    return "".join(out)


if __name__ == "__main__":
    a = sys.argv[1:] or ["enc", "3", "WEAREDISCOVEREDFLEEATONCE"]
    f = encrypt if a[0] == "enc" else decrypt
    print(f(a[2], int(a[1])))
