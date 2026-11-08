"""Pretty-print CSV files as aligned tables, with sorting, filtering and column stats.

    python csvview.py data.csv                       # boxed table
    python csvview.py data.csv --sort age --desc     # sort by a column (numbers sort numerically)
    python csvview.py data.csv --where "city=Pécs"   # keep rows whose column matches
    python csvview.py data.csv --cols name,age       # pick columns
    python csvview.py data.csv --stats               # per-column summary
    python csvview.py --demo                         # built-in sample

The delimiter is sniffed (comma, semicolon, tab, pipe). Numeric columns are right-aligned.
"""
from __future__ import annotations

import csv
import io
import statistics
import sys
import unicodedata

DEMO = """name;city;age;score
Anna;Budapest;34;88.5
Bence;Pécs;27;92
Csilla;Szeged;41;79.25
Dávid;Budapest;19;95
Emese;Győr;30;
Ferenc;Pécs;52;67.5
"""


def to_number(s: str) -> float | None:
    try:
        return float(s.replace(",", ".")) if s.strip() else None
    except ValueError:
        return None


def width(s: str) -> int:
    """Display width (wide East Asian characters take two cells)."""
    return sum(2 if unicodedata.east_asian_width(ch) in "WF" else 1 for ch in s)


def read(text: str) -> tuple[list[str], list[list[str]]]:
    try:
        dialect = csv.Sniffer().sniff(text[:4096], delimiters=",;\t|")
    except csv.Error:
        dialect = csv.excel
    rows = [r for r in csv.reader(io.StringIO(text), dialect) if r]
    if not rows:
        return [], []
    header, body = rows[0], rows[1:]
    n = len(header)
    body = [(r + [""] * n)[:n] for r in body]
    return header, body


def is_numeric(col: list[str]) -> bool:
    vals = [v for v in col if v.strip()]
    return bool(vals) and all(to_number(v) is not None for v in vals)


def table(header: list[str], rows: list[list[str]]) -> list[str]:
    cols = list(zip(*([header] + rows))) if rows else [(h,) for h in header]
    widths = [max(width(v) for v in col) for col in cols]
    numeric = [is_numeric(list(col[1:])) for col in cols]

    def fmt(row: list[str]) -> str:
        cells = []
        for v, w, num in zip(row, widths, numeric):
            pad = " " * (w - width(v))
            cells.append(pad + v if num else v + pad)
        return "│ " + " │ ".join(cells) + " │"

    line = lambda l, m, r: l + m.join("─" * (w + 2) for w in widths) + r  # noqa: E731
    out = [line("┌", "┬", "┐"), fmt(header), line("├", "┼", "┤")]
    out += [fmt(r) for r in rows]
    out.append(line("└", "┴", "┘"))
    return out


def stats(header: list[str], rows: list[list[str]]) -> list[str]:
    out = []
    for i, h in enumerate(header):
        col = [r[i] for r in rows]
        filled = [v for v in col if v.strip()]
        if is_numeric(col):
            nums = [to_number(v) for v in filled]
            out.append(f"{h}: n={len(nums)} min={min(nums):g} max={max(nums):g} "
                       f"mean={statistics.fmean(nums):.3g} median={statistics.median(nums):g}"
                       + (f" missing={len(col) - len(filled)}" if len(filled) < len(col) else ""))
        else:
            counts: dict[str, int] = {}
            for v in filled:
                counts[v] = counts.get(v, 0) + 1
            top = sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))[:3]
            out.append(f"{h}: {len(counts)} distinct; top " + ", ".join(f"{k} ({n})" for k, n in top))
    return out


def apply(header, rows, sort=None, desc=False, where=None, cols=None):
    if where:
        key, _, val = where.partition("=")
        i = header.index(key)
        rows = [r for r in rows if r[i].lower() == val.lower()]
    if sort:
        i = header.index(sort)
        if is_numeric([r[i] for r in rows]):
            rows = sorted(rows, key=lambda r: (to_number(r[i]) is None, to_number(r[i]) or 0), reverse=desc)
        else:
            rows = sorted(rows, key=lambda r: r[i].lower(), reverse=desc)
    if cols:
        idx = [header.index(c) for c in cols.split(",")]
        header = [header[i] for i in idx]
        rows = [[r[i] for i in idx] for r in rows]
    return header, rows


def main(argv: list[str]) -> int:
    opts: dict[str, str | bool] = {}
    files = []
    it = iter(argv)
    for a in it:
        if a in ("--sort", "--where", "--cols"):
            opts[a[2:]] = next(it, "")
        elif a in ("--desc", "--stats", "--demo"):
            opts[a[2:]] = True
        else:
            files.append(a)
    if files:
        with open(files[0], encoding="utf-8-sig") as fh:
            text = fh.read()
    elif opts.get("demo") or sys.stdin.isatty():
        text = DEMO
    else:
        text = sys.stdin.read()
    header, rows = read(text)
    try:
        header, rows = apply(header, rows, opts.get("sort"), bool(opts.get("desc")), opts.get("where"),
                             opts.get("cols"))
    except ValueError as exc:
        print(f"unknown column: {exc}", file=sys.stderr)
        return 2
    print("\n".join(table(header, rows)))
    print(f"{len(rows)} row(s)")
    if opts.get("stats"):
        print("\n".join(stats(header, rows)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
