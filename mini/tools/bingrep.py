#!/usr/bin/env python3
"""bingrep - find a hex byte pattern (with ?? wildcards) or a text string in binary files.

Usage: bingrep.py "DE AD ?? EF" file ...     |     bingrep.py -t "text" file ...
"""
import re
import sys


def compile_hex(pattern: str) -> re.Pattern:
    toks = pattern.replace(",", " ").split()
    parts = []
    for t in toks:
        if t == "??":
            parts.append(b".")
        else:
            parts.append(re.escape(bytes([int(t, 16)])))
    return re.compile(b"".join(parts), re.DOTALL)


def find(data: bytes, rx: re.Pattern) -> list[int]:
    out, pos = [], 0
    while (m := rx.search(data, pos)):
        out.append(m.start())
        pos = m.start() + 1
    return out


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        assert find(b"\x00\xde\xad\x01\xef\xde\xad\xff\xef", compile_hex("DE AD ?? EF")) == [1, 5]
        assert find(b"hello hello", re.compile(re.escape(b"llo"))) == [2, 8]
        assert find(b"abc", compile_hex("ff")) == []
        print("ok")
        sys.exit()
    args = sys.argv[1:]
    text_mode = bool(args) and args[0] == "-t"
    if text_mode:
        args.pop(0)
    if len(args) < 2:
        sys.exit(__doc__)
    pat, files = args[0], args[1:]
    rx = re.compile(re.escape(pat.encode())) if text_mode else compile_hex(pat)
    for f in files:
        with open(f, "rb") as fh:
            for off in find(fh.read(), rx):
                print(f"{f}: 0x{off:08x}")
