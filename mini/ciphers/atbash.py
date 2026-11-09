"""Atbash cipher: A<->Z, B<->Y, ... Self-inverse. Usage: python atbash.py "text" """
import sys


def atbash(s: str) -> str:
    out = []
    for c in s:
        if c.isascii() and c.isalpha():
            base = ord("A") if c.isupper() else ord("a")
            out.append(chr(base + 25 - (ord(c) - base)))
        else:
            out.append(c)
    return "".join(out)


if __name__ == "__main__":
    text = " ".join(sys.argv[1:]) or "Wizard"
    print(atbash(text))
    assert atbash(atbash(text)) == text
