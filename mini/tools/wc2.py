#!/usr/bin/env python3
"""wc2 - count lines, words, chars, bytes and the longest line of files or stdin."""
import sys

def stats(text: str) -> dict:
    lines = text.split("\n")
    return {"lines": text.count("\n"), "words": len(text.split()), "chars": len(text),
            "bytes": len(text.encode()), "longest": max(map(len, lines), default=0)}

if __name__ == "__main__":
    if "--selftest" in sys.argv:
        assert stats("a b\nc\n") == {"lines": 2, "words": 3, "chars": 6, "bytes": 6, "longest": 3}
        print("ok"); sys.exit()
    for name in sys.argv[1:] or ["-"]:
        data = sys.stdin.read() if name == "-" else open(name, encoding="utf-8", errors="replace").read()
        s = stats(data)
        print(f"{s['lines']:>7} {s['words']:>7} {s['chars']:>8} {s['bytes']:>8} max{s['longest']:>5} {name}")
