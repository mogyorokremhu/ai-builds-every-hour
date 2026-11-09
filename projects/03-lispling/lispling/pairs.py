"""Dotted pairs: improper lists such as (1 2 . 3).

Proper lists stay Python lists. A Pair appears only when a cdr is not a list.
"""
from __future__ import annotations


class Pair:
    __slots__ = ("car", "cdr")

    def __init__(self, car, cdr):
        self.car, self.cdr = car, cdr

    def __eq__(self, o):
        return isinstance(o, Pair) and self.car == o.car and self.cdr == o.cdr

    def __hash__(self):
        return hash((repr(self.car), repr(self.cdr)))


def make_dotted(items: list, tail):
    """Build (items... . tail); a list tail collapses to a proper list."""
    if isinstance(tail, list):
        return items + tail
    res = tail
    for x in reversed(items):
        res = Pair(x, res)
    return res


def pair_to_string(p: Pair, fmt) -> str:
    parts = []
    while isinstance(p, Pair):
        parts.append(fmt(p.car))
        p = p.cdr
    return "(" + " ".join(parts) + " . " + fmt(p) + ")"
