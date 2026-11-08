#!/usr/bin/env python3
"""csvview — show a CSV file as an aligned table, with sorting, filtering and stats.

Usage:
    python csvview.py FILE [--sort COL[:desc]] [--where 'COL OP VALUE'] [--cols a,b,c]
                           [--head N] [--stats] [--md] [--delim ';']

* ``--where``  filters rows; OP is one of ``= != < <= > >= ~`` (``~`` = contains,
               case-insensitive). Numbers compare numerically. Repeatable (AND).
* ``--sort``   sorts numerically when every value in the column is a number.
* ``--stats``  per-column summary: type, non-empty count, distinct, min/max/mean.
* ``--md``     print a Markdown table instead of a box-drawn one.

The delimiter is sniffed automatically unless ``--delim`` is given. Numbers are
right-aligned, text left-aligned; ``-`` reads from standard input.
"""
from __future__ import annotations

import csv
import io
import statistics
import sys

OPS = {"=", "!=", "<", "<=", ">", ">=", "~"}


def num(s: str) -> float | None:
    try:
        return float(s.replace(",", "")) if s.strip() else None
    except ValueError:
        return None


def is_numeric(values: list[str]) -> bool:
    filled = [v for v in values if v.strip()]
    return bool(filled) and all(num(v) is not None for v in filled)


def parse_where(expr: str) -> tuple[str, str, str]:
    for op in sorted(OPS, key=len, reverse=True):
        if f" {op} " in expr:
            col, val = expr.split(f" {op} ", 1)
            return col.strip(), op, val.strip()
    raise ValueError(f"can't parse filter {expr!r} (use 'col op value', ops: {' '.join(sorted(OPS))})")


def matches(cell: str, op: str, val: str) -> bool:
    a, b = num(cell), num(val)
    if op == "~":
        return val.lower() in cell.lower()
    if a is not None and b is not None:
        x, y = a, b
    else:
        x, y = cell, val  # type: ignore[assignment]
    return {"=": x == y, "!=": x != y, "<": x < y, "<=": x <= y, ">": x > y, ">=": x >= y}[op]


def load(text: str, delim: str | None = None) -> tuple[list[str], list[list[str]]]:
    if delim is None:
        try:
            delim = csv.Sniffer().sniff(text[:4096], delimiters=",;\t|").delimiter
        except csv.Error:
            delim = ","
    rows = list(csv.reader(io.StringIO(text), delimiter=delim))
    if not rows:
        return [], []
    header, body = rows[0], rows[1:]
    width = len(header)
    body = [(r + [""] * width)[:width] for r in body if any(c.strip() for c in r)]
    return header, body


def column(header: list[str], name: str) -> int:
    if name in header:
        return header.index(name)
    low = [h.lower() for h in header]
    if name.lower() in low:
        return low.index(name.lower())
    if name.isdigit() and int(name) < len(header):
        return int(name)
    raise SystemExit(f"no column {name!r}; columns are: {', '.join(header)}")


def table(header: list[str], rows: list[list[str]], md: bool = False) -> list[str]:
    numeric = [is_numeric([r[i] for r in rows]) for i in range(len(header))]
    widths = [max([len(h)] + [len(r[i]) for r in rows]) for i, h in enumerate(header)]

    def fmt(cells: list[str]) -> list[str]:
        return [c.rjust(w) if n else c.ljust(w) for c, w, n in zip(cells, widths, numeric)]

    if md:
        out = ["| " + " | ".join(fmt(header)) + " |",
               "|" + "|".join(("-" * (w + 1) + ":") if n else ("-" * (w + 2)) for w, n in zip(widths, numeric)) + "|"]
        out += ["| " + " | ".join(fmt(r)) + " |" for r in rows]
        return out
    line = lambda l, m, r: l + m.join("─" * (w + 2) for w in widths) + r
    out = [line("┌", "┬", "┐"), "│ " + " │ ".join(h.center(w) for h, w in zip(header, widths)) + " │",
           line("├", "┼", "┤")]
    out += ["│ " + " │ ".join(fmt(r)) + " │" for r in rows]
    out.append(line("└", "┴", "┘"))
    return out


def stats(header: list[str], rows: list[list[str]]) -> list[list[str]]:
    out = []
    for i, h in enumerate(header):
        vals = [r[i] for r in rows]
        filled = [v for v in vals if v.strip()]
        if is_numeric(vals):
            ns = [num(v) for v in filled]
            out.append([h, "number", str(len(filled)), str(len(set(filled))), f"{min(ns):g}", f"{max(ns):g}",
                        f"{statistics.fmean(ns):.4g}"])
        else:
            top = max(sorted(set(filled)), key=filled.count) if filled else ""
            out.append([h, "text", str(len(filled)), str(len(set(filled))), "", "", f"most common: {top}"])
    return out


def main(argv: list[str]) -> int:
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__)
        return 0
    opts: dict[str, list[str]] = {}
    files = []
    it = iter(argv)
    for a in it:
        if a in ("--sort", "--where", "--cols", "--head", "--delim"):
            opts.setdefault(a, []).append(next(it))
        elif a.startswith("--"):
            opts[a] = []
        else:
            files.append(a)
    text = sys.stdin.read() if files[0] == "-" else open(files[0], encoding="utf-8-sig").read()
    header, rows = load(text, opts.get("--delim", [None])[0])
    for expr in opts.get("--where", []):
        col, op, val = parse_where(expr)
        i = column(header, col)
        rows = [r for r in rows if matches(r[i], op, val)]
    for spec in opts.get("--sort", []):
        name, _, order = spec.partition(":")
        i = column(header, name)
        if is_numeric([r[i] for r in rows]):
            key = lambda r: (num(r[i]) is None, num(r[i]) or 0.0)
        else:
            key = lambda r: r[i].lower()
        rows.sort(key=key, reverse=order == "desc")
    if "--cols" in opts:
        idx = [column(header, c) for c in opts["--cols"][0].split(",")]
        header = [header[i] for i in idx]
        rows = [[r[i] for i in idx] for r in rows]
    if "--stats" in opts:
        print("\n".join(table(["column", "type", "filled", "distinct", "min", "max", "mean / note"],
                              stats(header, rows), "--md" in opts)))
        return 0
    total = len(rows)
    if "--head" in opts:
        rows = rows[: int(opts["--head"][0])]
    print("\n".join(table(header, rows, "--md" in opts)))
    print(f"{len(rows)} of {total} rows")
    return 0


def _selftest() -> None:
    h, rows = load("name;age;city\nAda;36;London\nLinus;28;Helsinki\nGrace;85;New York\n")
    assert h == ["name", "age", "city"] and len(rows) == 3
    assert is_numeric([r[1] for r in rows]) and not is_numeric([r[0] for r in rows])
    assert parse_where("age >= 30") == ("age", ">=", "30")
    assert [r[0] for r in rows if matches(r[1], ">", "30")] == ["Ada", "Grace"]
    assert matches("New York", "~", "york")
    t = table(h, rows)
    assert t[0].startswith("┌") and "│  36 │" in t[3] and t[3].endswith("│")
    assert stats(h, rows)[1][4:6] == ["28", "85"]
    print("selftest ok")


if __name__ == "__main__":
    if sys.argv[1:] == ["--selftest"]:
        _selftest()
    else:
        sys.exit(main(sys.argv[1:]))
