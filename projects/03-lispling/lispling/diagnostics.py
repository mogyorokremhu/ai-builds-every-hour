"""Source-position aware reading: errors say `line:col` and show the line."""
from __future__ import annotations
import re
from .reader import TOKEN, QUOTES, atom
from .types import LispError

_STRING_START = re.compile(r'"')


class SourceError(LispError):
    """A LispError carrying a source position."""

    def __init__(self, msg: str, line: int, col: int, text: str = ""):
        self.msg, self.line, self.col, self.text = msg, line, col, text
        caret = f"\n  {text}\n  {' ' * (col - 1)}^" if text else ""
        super().__init__(f"{line}:{col}: {msg}{caret}")


def tokenize_pos(src: str):
    """Yield (token, line, col) with 1-based positions; comments skipped."""
    pos = 0
    lines = src.split("\n")
    n = len(src)
    while pos < n:
        m = TOKEN.match(src, pos)
        if not m:
            if src[pos:].strip() == "":
                return
            line = src.count("\n", 0, pos) + 1
            col = pos - (src.rfind("\n", 0, pos) + 1) + 1
            raise SourceError("unterminated string or bad token", line, col, lines[line - 1])
        start = m.start(1)
        pos = m.end()
        t = m.group(1)
        if t.startswith(";"):
            continue
        line = src.count("\n", 0, start) + 1
        col = start - (src.rfind("\n", 0, start) + 1) + 1
        yield t, line, col


def parse_checked(src: str) -> list:
    """Like reader.parse, but every syntax error reports line:col."""
    lines = src.split("\n")
    toks = list(tokenize_pos(src))

    def err(msg, i):
        _, ln, col = toks[i]
        return SourceError(msg, ln, col, lines[ln - 1])

    def read(i, opener=None):
        t = toks[i][0]
        if t == "(":
            out, j = [], i + 1
            while True:
                if j >= len(toks):
                    raise err("unclosed (", i)
                if toks[j][0] == ")":
                    return out, j + 1
                e, j = read(j)
                out.append(e)
        if t == ")":
            raise err("unexpected )", i)
        if t in QUOTES:
            if i + 1 >= len(toks):
                raise err(f"nothing to {QUOTES[t]}", i)
            e, j = read(i + 1)
            from .types import sym
            return [sym(QUOTES[t]), e], j
        return atom(t), i + 1

    out, i = [], 0
    while i < len(toks):
        e, i = read(i)
        out.append(e)
    return out
