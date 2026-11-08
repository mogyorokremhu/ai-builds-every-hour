#!/usr/bin/env python3
"""Classic ciphers: caesar, rot13, vigenere, atbash — plus a Caesar brute-forcer ranked by English-ness.

usage: cipher.py caesar -k 3 "text"      cipher.py vigenere -k LEMON -d "LXFOPV"
       cipher.py crack "Khoor Zruog"     cipher.py atbash "text"      cipher.py --selftest
"""
import argparse, sys

FREQ = "etaoinshrdlucmfwypvbgkjqxz"
COMMON = {"the", "and", "of", "to", "a", "in", "is", "it", "hello", "world", "you", "that", "for", "with", "this", "on", "are", "was"}

def shift(text, k):
    out = []
    for ch in text:
        if ch.isalpha() and ch.isascii():
            base = ord("A") if ch.isupper() else ord("a")
            out.append(chr((ord(ch) - base + k) % 26 + base))
        else:
            out.append(ch)
    return "".join(out)

def vigenere(text, key, decrypt=False):
    ks = [ord(c.lower()) - 97 for c in key if c.isalpha()]
    if not ks:
        raise ValueError("key needs letters")
    out, i = [], 0
    for ch in text:
        if ch.isalpha() and ch.isascii():
            out.append(shift(ch, -ks[i % len(ks)] if decrypt else ks[i % len(ks)]))
            i += 1
        else:
            out.append(ch)
    return "".join(out)

def atbash(text):
    return "".join(chr(ord("Z") - (ord(c) - ord("A"))) if c.isupper() and c.isascii() else
                   chr(ord("z") - (ord(c) - ord("a"))) if c.islower() and c.isascii() else c for c in text)

def score(text):
    """Higher = more English-like (letter-frequency rank match)."""
    letters = [c for c in text.lower() if "a" <= c <= "z"]
    if not letters:
        return 0.0
    base = sum(26 - FREQ.index(c) for c in letters) / len(letters)
    hits = sum(w.strip(".,!?;:'\"") in COMMON for w in text.lower().split())
    return base + 10 * hits

def crack(text):
    return sorted(((score(shift(text, -k)), k, shift(text, -k)) for k in range(26)), reverse=True)

def selftest():
    assert shift("Hello, World!", 3) == "Khoor, Zruog!"
    assert shift(shift("abcXYZ", 5), -5) == "abcXYZ"
    assert vigenere("ATTACKATDAWN", "LEMON") == "LXFOPVEFRNHR"
    assert vigenere("LXFOPVEFRNHR", "LEMON", True) == "ATTACKATDAWN"
    assert atbash(atbash("Hello")) == "Hello" and atbash("abc") == "zyx"
    assert crack("Khoor Zruog")[0][1] == 3
    assert crack(shift("the quick brown fox jumps over the lazy dog", 11))[0][1] == 11
    print("cipher: ok")

def main():
    if "--selftest" in sys.argv:
        return selftest()
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("mode", choices=["caesar", "rot13", "vigenere", "atbash", "crack"])
    ap.add_argument("text", nargs="?")
    ap.add_argument("-k", "--key", default="3")
    ap.add_argument("-d", "--decrypt", action="store_true")
    a = ap.parse_args()
    text = a.text if a.text is not None else sys.stdin.read()
    if a.mode == "caesar":
        print(shift(text, -int(a.key) if a.decrypt else int(a.key)))
    elif a.mode == "rot13":
        print(shift(text, 13))
    elif a.mode == "vigenere":
        print(vigenere(text, a.key, a.decrypt))
    elif a.mode == "atbash":
        print(atbash(text))
    else:
        for sc, k, t in crack(text)[:5]:
            print(f"shift {k:2d}  score {sc:5.2f}  {t}")

if __name__ == "__main__":
    main()
