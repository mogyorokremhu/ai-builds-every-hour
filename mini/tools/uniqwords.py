#!/usr/bin/env python3
"""uniqwords: list distinct words in files/stdin. Usage: uniqwords.py [-s] [-i] [files]  (-s sort, -i ignore case)"""
import re, sys

def uniq_words(text, ignore_case=False, sort=False):
    seen, out = set(), []
    for w in re.findall(r"[A-Za-z0-9_']+", text):
        k = w.lower() if ignore_case else w
        if k not in seen:
            seen.add(k); out.append(k)
    return sorted(out) if sort else out

def main(argv):
    flags = [a for a in argv if a.startswith("-")]
    files = [a for a in argv if not a.startswith("-")]
    text = "".join(open(f, encoding="utf-8").read() for f in files) if files else sys.stdin.read()
    print("\n".join(uniq_words(text, "-i" in flags, "-s" in flags)))

if __name__ == "__main__":
    assert uniq_words("a b A a", False) == ["a", "b", "A"]
    assert uniq_words("b A a", True, True) == ["a", "b"]
    main(sys.argv[1:])
