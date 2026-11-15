"""Keyword substitution cipher: alphabet starts with keyword. Usage: python keyword_cipher.py [-d] KEY "text" """
import sys
import string


def build_alphabet(key: str) -> str:
    seen = []
    for c in key.upper() + string.ascii_uppercase:
        if c.isascii() and c.isalpha() and c not in seen:
            seen.append(c)
    return "".join(seen)


def keyword(s: str, key: str, decrypt: bool = False) -> str:
    cipher = build_alphabet(key)
    plain = string.ascii_uppercase
    src, dst = (cipher, plain) if decrypt else (plain, cipher)
    out = []
    for c in s:
        if c.isascii() and c.isalpha():
            m = dst[src.index(c.upper())]
            out.append(m if c.isupper() else m.lower())
        else:
            out.append(c)
    return "".join(out)


if __name__ == "__main__":
    args = sys.argv[1:]
    dec = "-d" in args
    args = [x for x in args if x != "-d"]
    key = args[0] if args else "ZEBRAS"
    text = " ".join(args[1:]) or "Flee at once"
    res = keyword(text, key, dec)
    print(res)
    assert keyword(res, key, not dec) == text
