"""Bacon's cipher: each letter -> 5 symbols of A/B. Usage: python bacon.py [-d] "text" """
import sys
import string

ALPHA = string.ascii_uppercase


def encode(s: str) -> str:
    return " ".join(
        format(ALPHA.index(c), "05b").replace("0", "A").replace("1", "B")
        for c in s.upper() if c in ALPHA
    )


def decode(s: str) -> str:
    return "".join(ALPHA[int(g.replace("A", "0").replace("B", "1"), 2)] for g in s.upper().split())


if __name__ == "__main__":
    args = sys.argv[1:]
    if args and args[0] == "-d":
        print(decode(" ".join(args[1:]) or "AABBB AABAA ABABB ABABB ABBBA"))
    else:
        text = " ".join(args) or "hello"
        enc = encode(text)
        print(enc)
        assert decode(enc) == "".join(c for c in text.upper() if c in ALPHA)
