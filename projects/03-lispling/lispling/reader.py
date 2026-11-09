"""Tokenizer and parser: text -> nested Python lists."""
from __future__ import annotations
import re
from .types import LispError, sym

TOKEN = re.compile(r"""\s*(,@|[('`,)]|"(?:\\.|[^\\"])*"|;.*|[^\s('"`,;)]+)""")


def tokenize(src: str) -> list[str]:
    toks, pos = [], 0
    src = src.rstrip()
    while pos < len(src):
        m = TOKEN.match(src, pos)
        if not m:
            break
        pos = m.end()
        t = m.group(1)
        if not t.startswith(";"):
            toks.append(t)
    return toks


def atom(tok: str):
    if tok.startswith('"'):
        return bytes(tok[1:-1], "utf-8").decode("unicode_escape")
    if tok == "#t":
        return True
    if tok == "#f":
        return False
    for conv in (int, float):
        try:
            return conv(tok)
        except ValueError:
            pass
    return sym(tok)


QUOTES = {"'": "quote", "`": "quasiquote", ",": "unquote", ",@": "unquote-splicing"}


def read_from(toks: list[str], i: int = 0):
    """Parse one expression starting at toks[i]; return (expr, next_index)."""
    if i >= len(toks):
        raise LispError("unexpected end of input")
    t = toks[i]
    if t == "(":
        out, i = [], i + 1
        while True:
            if i >= len(toks):
                raise LispError("missing )")
            if toks[i] == ")":
                return out, i + 1
            e, i = read_from(toks, i)
            out.append(e)
    if t == ")":
        raise LispError("unexpected )")
    if t in QUOTES:
        e, j = read_from(toks, i + 1)
        return [sym(QUOTES[t]), e], j
    return atom(t), i + 1


def parse(src: str) -> list:
    """Parse a whole program into a list of expressions."""
    toks, i, out = tokenize(src), 0, []
    while i < len(toks):
        e, i = read_from(toks, i)
        out.append(e)
    return out
