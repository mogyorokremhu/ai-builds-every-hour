#!/usr/bin/env python3
"""Sort lines of stdin/file: -n numeric, -r reverse, -u unique, -l by length."""
import re, sys


def sort_lines(lines, numeric=False, reverse=False, unique=False, by_len=False):
    if unique:
        lines = list(dict.fromkeys(lines))
    if numeric:
        def key(s):
            m = re.search(r"-?\d+(?:\.\d+)?", s)
            return (0, float(m.group())) if m else (1, 0.0)
    elif by_len:
        key = len
    else:
        key = None
    return sorted(lines, key=key, reverse=reverse)


def main(argv):
    flags = {a for a in argv if a.startswith("-") and len(a) == 2}
    if "--selftest" in argv:
        assert sort_lines(["b", "a", "b"], unique=True) == ["a", "b"]
        assert sort_lines(["x10", "x9", "none"], numeric=True) == ["x9", "x10", "none"]
        assert sort_lines(["ccc", "a", "bb"], by_len=True, reverse=True) == ["ccc", "bb", "a"]
        print("ok")
        return
    files = [a for a in argv if not a.startswith("-")]
    text = open(files[0]).read() if files else sys.stdin.read()
    out = sort_lines(text.splitlines(), "-n" in flags, "-r" in flags, "-u" in flags, "-l" in flags)
    print("\n".join(out))


if __name__ == "__main__":
    main(sys.argv[1:])
