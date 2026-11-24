"""ROT-N / Atbash letter substitutions with round-trip self-check."""
import string


def rot(text: str, n: int = 13) -> str:
    out = []
    for c in text:
        if c in string.ascii_lowercase:
            out.append(chr((ord(c) - 97 + n) % 26 + 97))
        elif c in string.ascii_uppercase:
            out.append(chr((ord(c) - 65 + n) % 26 + 65))
        else:
            out.append(c)
    return "".join(out)


def atbash(text: str) -> str:
    out = []
    for c in text:
        if c.islower() and c.isascii():
            out.append(chr(122 - (ord(c) - 97)))
        elif c.isupper() and c.isascii():
            out.append(chr(90 - (ord(c) - 65)))
        else:
            out.append(c)
    return "".join(out)


if __name__ == "__main__":
    s = "Hello, World!"
    assert rot(rot(s)) == s and atbash(atbash(s)) == s
    assert rot(s, 3) == "Khoor, Zruog!"
    print(rot(s), "|", atbash(s))
