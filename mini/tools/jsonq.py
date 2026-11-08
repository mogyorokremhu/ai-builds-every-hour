#!/usr/bin/env python3
"""jsonq — pretty-print, validate, minify and query JSON (a tiny dependency-free ``jq``).

Usage:
    python jsonq.py FILE [QUERY] [--min] [--sort] [--keys] [--indent N]
    cat data.json | python jsonq.py - 'users[0].name'

Queries are dotted paths with indexes and wildcards:
    users            the "users" field
    users[2].email   index into a list
    users[-1]        negative indexes count from the end
    users[*].name    map over every element (returns a list)
    meta."odd key"   quoted keys may contain dots and spaces

Invalid JSON is reported with the line, column and a caret under the offending spot.
``--keys`` lists the keys (or indexes) of the result instead of printing it.
"""
from __future__ import annotations

import json
import sys
from typing import Any

WILD = object()


class QueryError(Exception):
    pass


def parse_query(q: str) -> list[Any]:
    """'a.b[0][*]."c d"' -> ['a', 'b', 0, WILD, 'c d']"""
    out: list[Any] = []
    i, n = 0, len(q)
    while i < n:
        ch = q[i]
        if ch == ".":
            i += 1
        elif ch == "[":
            j = q.find("]", i)
            if j < 0:
                raise QueryError(f"unclosed '[' at {i}")
            inner = q[i + 1:j].strip()
            if inner == "*":
                out.append(WILD)
            else:
                try:
                    out.append(int(inner))
                except ValueError:
                    out.append(inner.strip("\"'"))
            i = j + 1
        elif ch in "\"'":
            j = q.find(ch, i + 1)
            if j < 0:
                raise QueryError(f"unclosed quote at {i}")
            out.append(q[i + 1:j])
            i = j + 1
        else:
            j = i
            while j < n and q[j] not in ".[":
                j += 1
            out.append(q[i:j])
            i = j
    return out


def run_query(data: Any, steps: list[Any], path: str = "$") -> Any:
    if not steps:
        return data
    step, rest = steps[0], steps[1:]
    if step is WILD:
        if isinstance(data, dict):
            items = list(data.values())
        elif isinstance(data, list):
            items = data
        else:
            raise QueryError(f"{path} is not a list or object; can't use [*]")
        return [run_query(v, rest, f"{path}[*]") for v in items]
    if isinstance(step, int):
        if not isinstance(data, list):
            raise QueryError(f"{path} is not a list; can't index [{step}]")
        try:
            return run_query(data[step], rest, f"{path}[{step}]")
        except IndexError:
            raise QueryError(f"{path}[{step}] is out of range (length {len(data)})") from None
    if not isinstance(data, dict):
        raise QueryError(f"{path} is not an object; no key {step!r}")
    if step not in data:
        close = [k for k in data if k.lower() == step.lower()]
        hint = f" (did you mean {close[0]!r}?)" if close else ""
        raise QueryError(f"{path} has no key {step!r}{hint}")
    return run_query(data[step], rest, f"{path}.{step}")


def describe_error(text: str, err: json.JSONDecodeError) -> str:
    lines = text.splitlines() or [""]
    line = lines[min(err.lineno, len(lines)) - 1]
    return f"invalid JSON: {err.msg} at line {err.lineno}, column {err.colno}\n  {line}\n  {' ' * (err.colno - 1)}^"


def main(argv: list[str]) -> int:
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__)
        return 0
    args = [a for a in argv if not a.startswith("--")]
    flags = [a for a in argv if a.startswith("--")]
    indent = 2
    if "--indent" in argv:
        idx = argv.index("--indent")
        indent = int(argv[idx + 1])
        args.remove(argv[idx + 1])
    src = args[0]
    text = sys.stdin.read() if src == "-" else open(src, encoding="utf-8").read()
    try:
        data = json.loads(text)
    except json.JSONDecodeError as err:
        print(describe_error(text, err), file=sys.stderr)
        return 1
    if len(args) > 1:
        try:
            data = run_query(data, parse_query(args[1]))
        except QueryError as exc:
            print(f"query error: {exc}", file=sys.stderr)
            return 2
    if "--keys" in flags:
        keys = list(data) if isinstance(data, dict) else list(range(len(data))) if isinstance(data, list) else []
        print("\n".join(map(str, keys)))
        return 0
    if "--min" in flags:
        print(json.dumps(data, separators=(",", ":"), sort_keys="--sort" in flags, ensure_ascii=False))
    else:
        print(json.dumps(data, indent=indent, sort_keys="--sort" in flags, ensure_ascii=False))
    return 0


def _selftest() -> None:
    doc = {"users": [{"name": "Ada", "tags": ["x"]}, {"name": "Linus", "tags": []}], "meta": {"a.b": 1}}
    assert parse_query('users[0].name') == ["users", 0, "name"]
    assert run_query(doc, parse_query("users[*].name")) == ["Ada", "Linus"]
    assert run_query(doc, parse_query("users[-1].name")) == "Linus"
    assert run_query(doc, parse_query('meta."a.b"')) == 1
    try:
        run_query(doc, parse_query("Users"))
    except QueryError as e:
        assert "did you mean 'users'" in str(e)
    print("selftest ok")


if __name__ == "__main__":
    if sys.argv[1:] == ["--selftest"]:
        _selftest()
    else:
        sys.exit(main(sys.argv[1:]))
