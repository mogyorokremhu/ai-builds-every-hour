"""Mutable fixed-size vectors (`vector`, `make-vector`, `vector-ref`, ...)."""
from __future__ import annotations
from .types import LispError, to_string


class Vector:
    """A fixed-size mutable sequence, printed as #(a b c)."""

    def __init__(self, items):
        self.items = list(items)

    def __eq__(self, other):
        return isinstance(other, Vector) and self.items == other.items

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return "#(" + " ".join(to_string(i) for i in self.items) + ")"


def _v(name, x) -> Vector:
    if not isinstance(x, Vector):
        raise LispError(f"{name}: expected vector, got {to_string(x)}")
    return x


def _idx(name, v: Vector, i) -> int:
    if isinstance(i, bool) or not isinstance(i, int):
        raise LispError(f"{name}: index must be an integer")
    if not 0 <= i < len(v.items):
        raise LispError(f"{name}: index {i} out of range (length {len(v.items)})")
    return i


def _make(n, fill=0):
    if isinstance(n, bool) or not isinstance(n, int) or n < 0:
        raise LispError("make-vector: size must be a non-negative integer")
    return Vector([fill] * n)


def _ref(v, i):
    _v("vector-ref", v)
    return v.items[_idx("vector-ref", v, i)]


def _set(v, i, x):
    _v("vector-set!", v)
    v.items[_idx("vector-set!", v, i)] = x
    return x


def _fill(v, x):
    _v("vector-fill!", v).items[:] = [x] * len(v.items)
    return v


def make() -> dict:
    return {
        "vector": lambda *a: Vector(a),
        "make-vector": _make,
        "vector?": lambda x: isinstance(x, Vector),
        "vector-length": lambda v: len(_v("vector-length", v).items),
        "vector-ref": _ref,
        "vector-set!": _set,
        "vector-fill!": _fill,
        "vector->list": lambda v: list(_v("vector->list", v).items),
        "list->vector": lambda l: Vector(l),
    }
