#!/usr/bin/env python3
"""rle - run-length encode/decode text (`rle.py -d` decodes; reads stdin or files). `--selftest` runs checks."""
import re
import sys

def encode(s: str) -> str:
    out, i = [], 0
    while i < len(s):
        j = i
        while j < len(s) and s[j] == s[i]: j += 1
        out.append(f"{j - i}{s[i]}"); i = j
    return "".join(out)

def decode(s: str) -> str:
    return "".join(c * int(n) for n, c in re.findall(r"(\d+)(\D|\d(?!\d))", s)) if s else ""

if __name__ == "__main__":
    if "--selftest" in sys.argv:
        assert encode("aaabccdddd") == "3a1b2c4d" and decode("3a1b2c4d") == "aaabccdddd"
        assert decode(encode("hello  world")) == "hello  world"; print("ok"); sys.exit()
    files = [a for a in sys.argv[1:] if not a.startswith("-")]
    text = "".join(open(f).read() for f in files) if files else sys.stdin.read()
    for line in text.splitlines(): print(decode(line) if "-d" in sys.argv else encode(line))
