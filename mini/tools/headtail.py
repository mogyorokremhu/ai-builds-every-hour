#!/usr/bin/env python3
"""Show the first and last N lines of a file/stdin with an elision marker: headtail.py [-n 5] [file]."""
import sys


def headtail(lines: list, n: int) -> list:
    if len(lines) <= 2 * n:
        return lines
    return lines[:n] + [f"... ({len(lines) - 2 * n} lines omitted) ..."] + lines[-n:]


def selftest() -> None:
    xs = [str(i) for i in range(10)]
    assert headtail(xs, 5) == xs
    assert headtail(xs, 2) == ["0", "1", "... (6 lines omitted) ...", "8", "9"]
    print("ok")


if __name__ == "__main__":
    a = sys.argv[1:]
    if "--selftest" in a:
        selftest()
        sys.exit()
    n = 5
    if "-n" in a:
        i = a.index("-n")
        n = int(a[i + 1])
        del a[i:i + 2]
    text = open(a[0]).read() if a else sys.stdin.read()
    print("\n".join(headtail(text.splitlines(), n)))
