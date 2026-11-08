"""A tiny jq-like JSON query tool with a hand-written path language.

    python jsonq.py data.json                         # pretty-print with colours
    python jsonq.py data.json '.users[0].name'        # index into objects/arrays
    python jsonq.py data.json '.users[].email'        # [] iterates
    python jsonq.py data.json '.users[?age>30].name'  # filter: ?key op value (= != > < >= <=)
    python jsonq.py data.json '.users | length'       # pipes: length, keys, sort, uniq, sum, first, last
    echo '{"a":[1,2,3]}' | python jsonq.py - '.a | sum'
    python jsonq.py --demo '.team[?role=dev].name'

Results are printed one per line (JSON-encoded, like ``jq -c`` when not a terminal).
"""
from __future__ import annotations

import json
import re
import sys
from typing import Any, Iterator

DEMO = {
    "project": "ai-builds-every-hour",
    "team": [
        {"name": "Ada", "role": "dev", "age": 36, "langs": ["python", "c"]},
        {"name": "Grace", "role": "lead", "age": 45, "langs": ["cobol"]},
        {"name": "Linus", "role": "dev", "age": 29, "langs": ["c", "shell"]},
    ],
    "stars": 42,
}

STEP = re.compile(r"""\.(?P<key>[A-Za-z_][\w-]*)|\[(?P<idx>-?\d+)\]|\[\](?P<all>)|\["(?P<qkey>[^"]*)"\]
                      |\[\?(?P<fkey>[\w-]+)\s*(?P<op>==|!=|>=|<=|=|>|<)\s*(?P<val>[^\]]+)\]""", re.X)

OPS = {
    "=": lambda a, b: a == b, "==": lambda a, b: a == b, "!=": lambda a, b: a != b,
    ">": lambda a, b: a > b, "<": lambda a, b: a < b, ">=": lambda a, b: a >= b, "<=": lambda a, b: a <= b,
}


class QueryError(Exception):
    pass


def literal(text: str) -> Any:
    text = text.strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return text.strip("'\"")


def walk(values: Iterator[Any], path: str) -> Iterator[Any]:
    pos = 0
    path = path.strip()
    if path in ("", "."):
        yield from values
        return
    steps = []
    while pos < len(path):
        m = STEP.match(path, pos)
        if not m:
            raise QueryError(f"bad path near {path[pos:]!r}")
        steps.append(m)
        pos = m.end()
    for m in steps:
        values = _apply(values, m)
    yield from values


def _apply(values: Iterator[Any], m: re.Match) -> Iterator[Any]:
    for v in values:
        if m.group("key") is not None or m.group("qkey") is not None:
            k = m.group("key") if m.group("key") is not None else m.group("qkey")
            if isinstance(v, dict) and k in v:
                yield v[k]
        elif m.group("idx") is not None:
            i = int(m.group("idx"))
            if isinstance(v, list) and -len(v) <= i < len(v):
                yield v[i]
        elif m.group("all") is not None:
            if isinstance(v, list):
                yield from v
            elif isinstance(v, dict):
                yield from v.values()
        else:
            want = literal(m.group("val"))
            op = OPS[m.group("op")]
            items = v if isinstance(v, list) else [v]
            for it in items:
                if isinstance(it, dict) and m.group("fkey") in it:
                    try:
                        if op(it[m.group("fkey")], want):
                            yield it
                    except TypeError:
                        continue


def pipe(values: list[Any], fn: str) -> list[Any]:
    fn = fn.strip()
    flat = lambda: [x for v in values for x in (v if isinstance(v, list) else [v])]  # noqa: E731
    if fn == "length":
        return [len(v) if isinstance(v, (list, dict, str)) else 0 for v in values]
    if fn == "keys":
        return [sorted(v) for v in values if isinstance(v, dict)]
    if fn == "sort":
        return [sorted(flat())]
    if fn == "uniq":
        out: list[Any] = []
        for x in flat():
            if x not in out:
                out.append(x)
        return [out]
    if fn == "sum":
        return [sum(x for x in flat() if isinstance(x, (int, float)))]
    if fn == "count":
        return [len(values)]
    if fn == "first":
        return values[:1]
    if fn == "last":
        return values[-1:]
    if fn.startswith("."):
        return list(walk(iter(values), fn))
    raise QueryError(f"unknown function {fn!r}")


def query(data: Any, q: str) -> list[Any]:
    parts = q.split("|")
    values = list(walk(iter([data]), parts[0]))
    for fn in parts[1:]:
        values = pipe(values, fn)
    return values


def colorize(text: str) -> str:
    pat = re.compile(r'("(?:\\.|[^"\\])*")(\s*:)?|\b(true|false|null)\b|(-?\d+(?:\.\d+)?(?:[eE][-+]?\d+)?)')

    def sub(m: re.Match) -> str:
        if m.group(1):
            return (f"\033[34m{m.group(1)}\033[0m{m.group(2)}" if m.group(2) else f"\033[32m{m.group(1)}\033[0m")
        if m.group(3):
            return f"\033[35m{m.group(3)}\033[0m"
        return f"\033[33m{m.group(4)}\033[0m"

    return pat.sub(sub, text)


def main(argv: list[str]) -> int:
    if not argv:
        print(__doc__)
        return 2
    if argv[0] == "--demo":
        data, q = DEMO, (argv[1] if len(argv) > 1 else ".")
    else:
        src = sys.stdin.read() if argv[0] == "-" else open(argv[0], encoding="utf-8").read()
        data, q = json.loads(src), (argv[1] if len(argv) > 1 else ".")
    try:
        results = query(data, q)
    except QueryError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    tty = sys.stdout.isatty()
    for r in results:
        text = json.dumps(r, indent=2 if tty else None, ensure_ascii=False)
        print(colorize(text) if tty else text)
    return 0 if results else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
