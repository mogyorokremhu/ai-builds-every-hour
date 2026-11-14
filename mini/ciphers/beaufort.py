"""Beaufort cipher: like Vigenere but C = (K - P) mod 26; self-reciprocal.
Usage: python beaufort.py KEY "text" """
import sys


def beaufort(text: str, key: str) -> str:
    key = [ord(k) - 65 for k in key.upper() if k.isalpha()]
    out, i = [], 0
    for c in text:
        if c.isascii() and c.isalpha():
            base = 65 if c.isupper() else 97
            out.append(chr(base + (key[i % len(key)] - (ord(c) - base)) % 26))
            i += 1
        else:
            out.append(c)
    return "".join(out)


if __name__ == "__main__":
    key = sys.argv[1] if len(sys.argv) > 1 else "FORTIFICATION"
    text = " ".join(sys.argv[2:]) or "Defend the east wall"
    enc = beaufort(text, key)
    print(enc)
    assert beaufort(enc, key) == text
