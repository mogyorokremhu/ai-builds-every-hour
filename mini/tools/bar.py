#!/usr/bin/env python3
"""Bar chart from `label value` lines on stdin: `printf 'a 3\nb 7\n' | python bar.py`."""
import sys

def chart(rows, width=40):
    top = max(v for _, v in rows) or 1
    pad = max(len(l) for l, _ in rows)
    return "\n".join(f"{l:>{pad}} | {'█' * round(v / top * width)} {v:g}" for l, v in rows)

if __name__ == "__main__":
    if sys.argv[1:] == ["--selftest"]:
        out = chart([("a", 1), ("b", 2)], 10).splitlines()
        assert out[1].count("█") == 10 and out[0].count("█") == 5; print("ok")
    else:
        rows = [(p[0], float(p[1])) for p in (l.split() for l in sys.stdin) if len(p) >= 2]
        print(chart(rows))
