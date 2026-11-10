"""Columnar transposition cipher. Usage: python columnar.py [-d] KEY "text" """
import sys


def _order(key: str) -> list[int]:
    return sorted(range(len(key)), key=lambda i: (key[i], i))


def encrypt(text: str, key: str) -> str:
    return "".join(text[c::len(key)] for c in _order(key))


def decrypt(text: str, key: str) -> str:
    n, k = len(text), len(key)
    rows, extra = divmod(n, k)
    res = [""] * n
    pos = 0
    for c in _order(key):
        length = rows + (1 if c < extra else 0)
        for j in range(length):
            res[c + j * k] = text[pos + j]
        pos += length
    return "".join(res)


if __name__ == "__main__":
    args = sys.argv[1:]
    dec = "-d" in args
    args = [a for a in args if a != "-d"]
    key = args[0] if args else "ZEBRA"
    text = " ".join(args[1:]) or "WEAREDISCOVEREDFLEEATONCE"
    out = decrypt(text, key) if dec else encrypt(text, key)
    print(out)
    assert (encrypt(out, key) if dec else decrypt(out, key)) == text
