#!/usr/bin/env python3
"""Character class summary of text: letters, digits, spaces, punctuation, non-ASCII."""
import sys
from collections import Counter


def classify(text):
    c = Counter()
    for ch in text:
        if ch.isalpha():
            c["letters"] += 1
        elif ch.isdigit():
            c["digits"] += 1
        elif ch.isspace():
            c["whitespace"] += 1
        else:
            c["punctuation/other"] += 1
        if ord(ch) > 127:
            c["non-ascii"] += 1
    return c


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        r = classify("ab 12!é")
        assert r["letters"] == 3 and r["digits"] == 2 and r["whitespace"] == 1
        assert r["punctuation/other"] == 1 and r["non-ascii"] == 1
        print("ok")
    else:
        for k, v in classify(sys.stdin.read()).most_common():
            print(f"{k:18}{v}")
