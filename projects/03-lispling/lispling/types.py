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
    if isinstance(x, Symbol):
        return str(x)
    if isinstance(x, str):
        return '"' + x.replace("\\", "\\\\").replace('"', '\\"') + '"'
    if isinstance(x, float) and x.is_integer():
        return str(int(x))
    if isinstance(x, Lambda):
        return f"#<lambda {x.name or 'anonymous'}>"
    if callable(x):
        return "#<builtin>"
    return str(x)


class Lambda:
    """A user-defined procedure (closure)."""

    def __init__(self, params, body, env, name=""):
        self.params, self.body, self.env, self.name = params, body, env, name


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
