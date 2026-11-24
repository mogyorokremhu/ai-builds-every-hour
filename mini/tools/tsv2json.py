#!/usr/bin/env python3
"""Convert TSV (header row) from stdin or a file to a JSON array of objects."""
import json
import sys


def convert(text: str) -> list:
    lines = [l for l in text.splitlines() if l.strip()]
    if not lines:
        return []
    head = lines[0].split("\t")
    rows = []
    for l in lines[1:]:
        cells = l.split("\t")
        cells += [""] * (len(head) - len(cells))
        rows.append(dict(zip(head, cells)))
    return rows


def selftest() -> None:
    assert convert("a\tb\n1\t2\n3\n") == [{"a": "1", "b": "2"}, {"a": "3", "b": ""}]
    assert convert("") == []
    print("ok")


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        selftest()
    else:
        src = open(sys.argv[1]).read() if len(sys.argv) > 1 else sys.stdin.read()
        print(json.dumps(convert(src), indent=2))
