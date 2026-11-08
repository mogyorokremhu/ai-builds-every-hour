#!/usr/bin/env python3
"""Rotate/reverse text: `rot.py -r` reverses lines, `-w` reverses word order, `-c` reverses characters."""
import sys

def transform(text, mode):
    lines = text.splitlines()
    if mode == "r": return "\n".join(reversed(lines))
    if mode == "w": return "\n".join(" ".join(reversed(l.split())) for l in lines)
    return "\n".join(l[::-1] for l in lines)

if __name__ == "__main__":
    if sys.argv[1:] == ["--selftest"]:
        assert transform("a b\nc d", "r") == "c d\na b"
        assert transform("a b\nc d", "w") == "b a\nd c"
        assert transform("ab\ncd", "c") == "ba\ndc"; print("ok")
    else:
        mode = (sys.argv[1].lstrip("-") if len(sys.argv) > 1 else "c")[:1] or "c"
        print(transform(sys.stdin.read(), mode))
