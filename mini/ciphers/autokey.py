"""Autokey cipher: the key is the keyword followed by the plaintext itself.
Usage: python autokey.py KEY "text" [-d] """
import sys


def _letters(s: str) -> list[int]:
    return [ord(c) - 65 for c in s.upper() if c.isalpha()]


def autokey(text: str, key: str, decrypt: bool = False) -> str:
    stream = _letters(key)
    out, i = [], 0
    for c in text:
        if c.isascii() and c.isalpha():
            base = 65 if c.isupper() else 97
            p = ord(c) - base
            k = stream[i]
            if decrypt:
                p = (p - k) % 26
                stream.append(p)
                out.append(chr(base + p))
            else:
                stream.append(p)
                out.append(chr(base + (p + k) % 26))
            i += 1
        else:
            out.append(c)
    return "".join(out)


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if a != "-d"]
    dec = "-d" in sys.argv
    key = args[0] if args else "QUEENLY"
    text = " ".join(args[1:]) or "Attack at dawn"
    print(autokey(text, key, dec))
    if not dec:
        assert autokey(autokey(text, key), key, True) == text
