"""A TOML subset parser: [tables], [a.b] nested tables, strings, ints, floats,
bools, and flat arrays; checked against tomllib (Python 3.11+ when available)."""
import re


def _value(s: str):
    s = s.strip()
    if s.startswith('"') and s.endswith('"') and len(s) >= 2:
        return bytes(s[1:-1], "utf-8").decode("unicode_escape")
    if s.startswith("'") and s.endswith("'"):
        return s[1:-1]
    if s == "true":
        return True
    if s == "false":
        return False
    if s.startswith("["):
        inner = s[1:-1].strip()
        return [_value(p) for p in _split_top(inner)] if inner else []
    t = s.replace("_", "")
    if re.fullmatch(r"[+-]?\d+", t):
        return int(t)
    return float(t)


def _split_top(s: str) -> list[str]:
    parts, cur, q, depth = [], "", None, 0
    for c in s:
        if q:
            cur += c
            if c == q:
                q = None
        elif c in "\"'":
            q = c
            cur += c
        elif c == "[":
            depth += 1
            cur += c
        elif c == "]":
            depth -= 1
            cur += c
        elif c == "," and depth == 0:
            parts.append(cur)
            cur = ""
        else:
            cur += c
    if cur.strip():
        parts.append(cur)
    return parts


def _strip_comment(line: str) -> str:
    q = None
    for i, c in enumerate(line):
        if q:
            if c == q:
                q = None
        elif c in "\"'":
            q = c
        elif c == "#":
            return line[:i]
    return line


def loads(text: str) -> dict:
    root: dict = {}
    cur = root
    for raw in text.splitlines():
        line = _strip_comment(raw).strip()
        if not line:
            continue
        if line.startswith("[") and line.endswith("]") and not line.startswith("[["):
            cur = root
            for key in line[1:-1].strip().split("."):
                cur = cur.setdefault(key.strip(), {})
        else:
            k, _, v = line.partition("=")
            cur[k.strip()] = _value(v)
    return root


if __name__ == "__main__":
    doc = '''
title = "Demo"  # comment
debug = false
[server]
host = 'localhost'
port = 8_080
ratio = 0.75
tags = ["a", "b # not comment", "c"]
[server.tls]
enabled = true
matrix = [[1, 2], [3]]
'''
    mine = loads(doc)
    print(mine)
    try:
        import tomllib
        assert mine == tomllib.loads(doc)
        print("matches tomllib")
    except ImportError:
        pass
    assert mine["server"]["tls"]["matrix"] == [[1, 2], [3]]
    assert mine["server"]["port"] == 8080
    print("toml_lite_parser: all checks passed")
