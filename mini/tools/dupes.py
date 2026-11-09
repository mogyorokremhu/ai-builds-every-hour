#!/usr/bin/env python3
"""Find duplicate files under a directory by size then SHA-256.

Usage: dupes.py [DIR] [--selftest]
"""
from __future__ import annotations
import hashlib
import os
import sys
import tempfile
from collections import defaultdict


def sha(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def find_dupes(root: str) -> list[list[str]]:
    """Return groups of paths with identical content."""
    by_size: dict[int, list[str]] = defaultdict(list)
    for d, _, files in os.walk(root):
        for n in files:
            p = os.path.join(d, n)
            if os.path.isfile(p) and not os.path.islink(p):
                by_size[os.path.getsize(p)].append(p)
    groups = []
    for paths in by_size.values():
        if len(paths) < 2:
            continue
        by_hash: dict[str, list[str]] = defaultdict(list)
        for p in paths:
            by_hash[sha(p)].append(p)
        groups += [sorted(g) for g in by_hash.values() if len(g) > 1]
    return sorted(groups)


def selftest() -> None:
    with tempfile.TemporaryDirectory() as t:
        for name, data in [("a", b"x"), ("b", b"x"), ("c", b"y"), ("d", b"xx")]:
            open(os.path.join(t, name), "wb").write(data)
        g = find_dupes(t)
        assert len(g) == 1 and [os.path.basename(p) for p in g[0]] == ["a", "b"], g
    print("ok")


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        selftest()
    else:
        root = next((a for a in sys.argv[1:] if not a.startswith("-")), ".")
        groups = find_dupes(root)
        for g in groups:
            print(f"{len(g)} copies, {os.path.getsize(g[0])} bytes:")
            for p in g:
                print("  " + p)
        print(f"{len(groups)} duplicate group(s)")
