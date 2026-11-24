"""Porta cipher (reciprocal, 13 alphabets). Usage: python porta.py KEY "text" """
import sys


def porta(s: str, key: str) -> str:
    key = [c for c in key.upper() if c.isalpha()]
    if not key:
        raise ValueError("key must contain letters")
    out, i = [], 0
    for c in s:
        if c.isascii() and c.isalpha():
            k = (ord(key[i % len(key)]) - 65) // 2
            x = ord(c.upper()) - 65
            y = (x - k) % 13 + 13 if x < 13 else (x + k) % 13
            r = chr(y + 65)
            out.append(r if c.isupper() else r.lower())
            i += 1
        else:
            out.append(c)
    return "".join(out)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    enc = porta(" ".join(sys.argv[2:]), sys.argv[1])
    print(enc)
    assert porta(enc, sys.argv[1]) == " ".join(sys.argv[2:]), "not reciprocal!"
