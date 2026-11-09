"""Primitive procedures."""
from __future__ import annotations
import math
import operator
from functools import reduce
from .pairs import Pair
from .types import LispError, Env, sym, to_string


def _num(f):
    def g(*a):
        for x in a:
            if isinstance(x, bool) or not isinstance(x, (int, float)):
                raise LispError(f"expected number, got {to_string(x)}")
        return f(*a)
    return g


def _div(a, *r):
    if not r:
        r, a = (a,), 1
    for d in r:
        if d == 0:
            raise LispError("division by zero")
        a = a // d if isinstance(a, int) and isinstance(d, int) and a % d == 0 else a / d
    return a


def _cmp(op):
    return _num(lambda *a: all(op(x, y) for x, y in zip(a, a[1:])))


def _car(x):
    if isinstance(x, Pair):
        return x.car
    if not isinstance(x, list) or not x:
        raise LispError("car of empty or non-list")
    return x[0]


def _cdr(x):
    if isinstance(x, Pair):
        return x.cdr
    if not isinstance(x, list) or not x:
        raise LispError("cdr of empty or non-list")
    return x[1:]


def _cons(a, b):
    if not isinstance(b, list):
        return Pair(a, b)
    return [a] + b


def install(env: Env, out=print) -> None:
    env.update({
        "+": _num(lambda *a: sum(a)),
        "-": _num(lambda a, *r: -a if not r else reduce(operator.sub, r, a)),
        "*": _num(lambda *a: reduce(operator.mul, a, 1)),
        "/": _num(_div),
        "mod": _num(operator.mod), "abs": _num(abs),
        "min": _num(min), "max": _num(max), "sqrt": _num(math.sqrt),
        "=": _cmp(operator.eq), "<": _cmp(operator.lt), ">": _cmp(operator.gt),
        "<=": _cmp(operator.le), ">=": _cmp(operator.ge),
        "not": lambda x: x is False,
        "car": _car, "cdr": _cdr, "cons": _cons,
        "list": lambda *a: list(a),
        "length": lambda x: len(x),
        "append": lambda *a: [i for l in a for i in l],
        "null?": lambda x: x == [],
        "list?": lambda x: isinstance(x, list),
        "pair?": lambda x: isinstance(x, Pair) or (isinstance(x, list) and len(x) > 0),
        "number?": lambda x: isinstance(x, (int, float)) and not isinstance(x, bool),
        "string?": lambda x: isinstance(x, str) and not isinstance(x, type(sym("a"))),
        "symbol?": lambda x: type(x).__name__ == "Symbol",
        "equal?": lambda a, b: a == b,
        "display": lambda *a: out(" ".join(x if isinstance(x, str) and type(x).__name__ != "Symbol" else to_string(x) for x in a)),
        "string-append": lambda *a: "".join(a),
    })
