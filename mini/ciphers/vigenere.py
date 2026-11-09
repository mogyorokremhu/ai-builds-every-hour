"""Vigenere cipher: python vigenere.py enc KEY "text" | dec KEY "text" """
import sys


def vig(text: str, key: str, sign: int = 1) -> str:
    out, i = [], 0
    for ch in text:
        if ch.isalpha() and ch.isascii():
            base = 65 if ch.isupper() else 97
            k = ord(key[i % len(key)].lower()) - 97
            out.append(chr((ord(ch) - base + sign * k) % 26 + base))
            i += 1
        else:
            out.append(ch)
    return "".join(out)


if __name__ == "__main__":
    a = sys.argv[1:] or ["enc", "lemon", "Attack at dawn"]
    c = vig(a[2], a[1], 1 if a[0] == "enc" else -1)
    print(c)
    if len(sys.argv) == 1:
        print(vig(c, "lemon", -1))
