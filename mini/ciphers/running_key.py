"""Running-key cipher: a long text acts as the key. Usage: python running_key.py [-d] KEYTEXT "text" """
import sys


def running_key(s: str, keytext: str, decrypt: bool = False) -> str:
    key = [ord(c) - 65 for c in keytext.upper() if c.isascii() and c.isalpha()]
    if not key:
        raise ValueError("key text must contain letters")
    out, i = [], 0
    for c in s:
        if c.isascii() and c.isalpha():
            k = key[i % len(key)] * (-1 if decrypt else 1)
            base = 65 if c.isupper() else 97
            out.append(chr((ord(c) - base + k) % 26 + base))
            i += 1
        else:
            out.append(c)
    return "".join(out)


if __name__ == "__main__":
    args = sys.argv[1:]
    d = bool(args and args[0] == "-d")
    if d:
        args = args[1:]
    if len(args) < 2:
        sys.exit(__doc__)
    print(running_key(" ".join(args[1:]), args[0], d))
