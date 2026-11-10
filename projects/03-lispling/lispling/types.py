"""Core data types."""
from __future__ import annotations


class LispError(Exception):
    """Any error raised while reading or evaluating Lispling code."""


class Symbol(str):
    """An interned symbol; compared by name."""
    __slots__ = ()


_table: dict[str, Symbol] = {}


def sym(name: str) -> Symbol:
    if name not in _table:
        _table[name] = Symbol(name)
    return _table[name]


def to_string(x: object) -> str:
    """Render a value the way the REPL prints it."""
    if x is True:
        return "#t"
    if x is False:
        return "#f"
    if isinstance(x, list):
        return "(" + " ".join(to_string(i) for i in x) + ")"
    if type(x).__name__ == "Pair":
        from .pairs import pair_to_string
        return pair_to_string(x, to_string)
    if isinstance(x, Symbol):
        return str(x)
    if isinstance(x, str):
        return '"' + x.replace("\\", "\\\\").replace('"', '\\"') + '"'
    if isinstance(x, float) and x.is_integer():
        return str(int(x))
    if isinstance(x, Macro):
        return f"#<macro {x.name}>"
    if isinstance(x, Lambda):
        return f"#<lambda {x.name or 'anonymous'}>"
    if type(x).__name__ == "HashTable":
        return f"#<hash-table {len(x.d)}>"
    if type(x).__name__ == "Vector":
        return repr(x)
    if callable(x):
        return "#<builtin>"
    return str(x)


def split_params(p):
    """Split a parameter spec into (fixed names, rest name or None).

    Accepts a list ``(a b)``, a dotted pair ``(a b . r)`` or a bare symbol ``args``.
    """
    from .pairs import Pair
    if isinstance(p, str):
        return [], p
    if isinstance(p, Pair):
        fixed = []
        while isinstance(p, Pair):
            fixed.append(p.car)
            p = p.cdr
        return fixed, p
    return list(p), None


def bind_params(env, params, rest, args, name=""):
    """Bind args to params (and the rest list) in env, checking arity."""
    n = len(params)
    if rest is None:
        if len(args) != n:
            raise LispError(f"{name or 'lambda'} expects {n} args, got {len(args)}")
    elif len(args) < n:
        raise LispError(f"{name or 'lambda'} expects at least {n} args, got {len(args)}")
    env.update(zip(params, args))
    if rest is not None:
        env[rest] = list(args[n:])


class Lambda:
    """A user-defined procedure (closure)."""

    def __init__(self, params, body, env, name=""):
        self.params, self.rest = split_params(params)
        self.body, self.env, self.name = body, env, name


class Macro(Lambda):
    """A non-hygienic macro: receives unevaluated forms, returns a form."""


class Env(dict):
    """A scope: a dict plus a parent link."""

    def __init__(self, parent: "Env | None" = None):
        super().__init__()
        self.parent = parent

    def find(self, name: str) -> "Env":
        e: Env | None = self
        while e is not None:
            if name in e:
                return e
            e = e.parent
        raise LispError(f"unbound symbol: {name}")
