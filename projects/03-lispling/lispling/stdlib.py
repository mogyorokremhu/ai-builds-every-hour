"""Strings, association lists and hash tables.

Characters are represented as one-character strings (there is no separate
char type). Hash tables wrap a dict keyed by a frozen form of the Lispling
value, so lists and strings both work as keys.
"""
from __future__ import annotations
import math
from .types import LispError, Symbol, sym, to_string


class HashTable:
    def __init__(self):
        self.d: dict = {}

    def __repr__(self):
        return f"#<hash-table {len(self.d)}>"


def _is_str(x) -> bool:
    return isinstance(x, str) and not isinstance(x, Symbol)


def _s(name, x):
    if not _is_str(x):
        raise LispError(f"{name}: expected string, got {to_string(x)}")
    return x


def _i(name, x):
    if isinstance(x, bool) or not isinstance(x, int):
        raise LispError(f"{name}: expected integer, got {to_string(x)}")
    return x


def _freeze(k):
    if isinstance(k, list):
        return ("list", tuple(_freeze(i) for i in k))
    return (type(k).__name__, k)


def _ht(name, h):
    if not isinstance(h, HashTable):
        raise LispError(f"{name}: expected hash table, got {to_string(h)}")
    return h.d


def _substring(s, start, end=None):
    _s("substring", s)
    end = len(s) if end is None else end
    if not (0 <= _i("substring", start) <= _i("substring", end) <= len(s)):
        raise LispError(f"substring: bad range {start}..{end} for length {len(s)}")
    return s[start:end]


def _string_ref(s, i):
    _s("string-ref", s)
    if not 0 <= _i("string-ref", i) < len(s):
        raise LispError(f"string-ref: index {i} out of range")
    return s[i]


def _string_to_number(s):
    _s("string->number", s)
    for conv in (int, float):
        try:
            return conv(s)
        except ValueError:
            pass
    return False


def _assoc(key, alist):
    if not isinstance(alist, list):
        raise LispError("assoc: expected an association list")
    for p in alist:
        if isinstance(p, list) and p and p[0] == key and type(p[0]) is type(key):
            return p
    return False


def _hash_ref(h, k, *default):
    d = _ht("hash-ref", h)
    fk = _freeze(k)
    if fk in d:
        return d[fk][1]
    if default:
        return default[0]
    raise LispError(f"hash-ref: no value for key {to_string(k)}")


def _hash_set(h, k, v):
    _ht("hash-set!", h)[_freeze(k)] = (k, v)
    return []


def _hash_remove(h, k):
    _ht("hash-remove!", h).pop(_freeze(k), None)
    return []


def _radix(n, r):
    n, r = int(n), int(r)
    if not 2 <= r <= 36:
        raise ValueError("number->string-radix: radix must be 2..36")
    digits = "0123456789abcdefghijklmnopqrstuvwxyz"
    sign, n = ("-" if n < 0 else ""), abs(n)
    out = ""
    while True:
        n, d = divmod(n, r)
        out = digits[d] + out
        if n == 0:
            return sign + out


def _n(name, x):
    if isinstance(x, bool) or not isinstance(x, (int, float)):
        raise TypeError(f"{name}: expected a number, got {x!r}")
    return x


def _int_fn(name, f):
    def g(*args):
        for a in args:
            if isinstance(_n(name, a), float) and a != int(a):
                raise TypeError(f"{name}: expected an integer, got {a!r}")
        return f(*[int(a) for a in args])
    return g


def _tdiv(a, b):
    if b == 0:
        raise LispError("division by zero")
    q = abs(a) // abs(b)
    return q if (a < 0) == (b < 0) else -q


def _expt(a, b):
    return _n("expt", a) ** _n("expt", b)


def _round_half_even(x):
    return int(round(_n("round", x)))


def make() -> dict:
    return {
        # numbers
        "gcd": lambda *a: math.gcd(*[int(_n("gcd", x)) for x in a]),
        "lcm": lambda *a: math.lcm(*[int(_n("lcm", x)) for x in a]),
        "quotient": _int_fn("quotient", lambda a, b: _tdiv(a, b)),
        "remainder": _int_fn("remainder", lambda a, b: a - b * _tdiv(a, b)),
        "modulo": _int_fn("modulo", lambda a, b: a % b),
        "expt": _expt,
        "floor": lambda x: math.floor(_n("floor", x)),
        "ceiling": lambda x: math.ceil(_n("ceiling", x)),
        "truncate": lambda x: math.trunc(_n("truncate", x)),
        "round": _round_half_even,
        "exact->inexact": lambda x: float(_n("exact->inexact", x)),
        "inexact->exact": lambda x: int(_n("inexact->exact", x)),
        "number->string-radix": lambda n, r: _radix(_n("number->string-radix", n), r),
        # strings
        "string-length": lambda s: len(_s("string-length", s)),
        "substring": _substring,
        "string-ref": _string_ref,
        "string-upcase": lambda s: _s("string-upcase", s).upper(),
        "string-downcase": lambda s: _s("string-downcase", s).lower(),
        "string-trim": lambda s: _s("string-trim", s).strip(),
        "string-pad-left": lambda s, n, c=" ": _s("string-pad-left", s).rjust(_i("string-pad-left", n), c),
        "string-pad-right": lambda s, n, c=" ": _s("string-pad-right", s).ljust(_i("string-pad-right", n), c),
        "string-prefix?": lambda p, s: _s("string-prefix?", s).startswith(_s("string-prefix?", p)),
        "string-suffix?": lambda p, s: _s("string-suffix?", s).endswith(_s("string-suffix?", p)),
        "string-reverse": lambda s: _s("string-reverse", s)[::-1],
        "string-repeat": lambda s, n: _s("string-repeat", s) * _i("string-repeat", n),
        "string-contains?": lambda s, t: _s("string-contains?", t) in _s("string-contains?", s),
        "string-index": lambda s, t: _s("string-index", s).find(_s("string-index", t)),
        "string-replace": lambda s, a, b: _s("string-replace", s).replace(_s("string-replace", a), _s("string-replace", b)),
        "string-split": lambda s, sep=" ": (_s("string-split", s).split(sep) if sep else list(s)),
        "string-join": lambda l, sep="": _s("string-join", sep).join(_s("string-join", x) for x in l),
        "string=?": lambda a, b: _s("string=?", a) == _s("string=?", b),
        "string<?": lambda a, b: _s("string<?", a) < _s("string<?", b),
        "string>?": lambda a, b: _s("string>?", a) > _s("string>?", b),
        "string<=?": lambda a, b: _s("string<=?", a) <= _s("string<=?", b),
        "string>=?": lambda a, b: _s("string>=?", a) >= _s("string>=?", b),
        "string-ci=?": lambda a, b: _s("string-ci=?", a).lower() == _s("string-ci=?", b).lower(),
        "string-trim-left": lambda s: _s("string-trim-left", s).lstrip(),
        "string-trim-right": lambda s: _s("string-trim-right", s).rstrip(),
        "string-titlecase": lambda s: _s("string-titlecase", s).title(),
        "string-count": lambda s, t: _s("string-count", s).count(_s("string-count", t)) if t else 0,
        "char-alphabetic?": lambda c: _s("char-alphabetic?", c).isalpha(),
        "char-numeric?": lambda c: _s("char-numeric?", c).isdigit(),
        "char-whitespace?": lambda c: _s("char-whitespace?", c).isspace(),
        "char-upper-case?": lambda c: _s("char-upper-case?", c).isupper(),
        "char-lower-case?": lambda c: _s("char-lower-case?", c).islower(),
        "char-upcase": lambda c: _s("char-upcase", c).upper(),
        "char-downcase": lambda c: _s("char-downcase", c).lower(),
        "char->integer": lambda c: ord(_s("char->integer", c)),
        "integer->char": lambda n: chr(_i("integer->char", n)),
        "string->list": lambda s: list(_s("string->list", s)),
        "list->string": lambda l: "".join(_s("list->string", c) for c in l),
        "string->number": _string_to_number,
        "number->string": lambda n: to_string(n),
        "string->symbol": lambda s: sym(_s("string->symbol", s)),
        "symbol->string": lambda x: str(x) if isinstance(x, Symbol) else _s("symbol->string", x),
        # association lists
        "assoc": _assoc, "assq": _assoc, "assv": _assoc,
        # hash tables
        "make-hash": lambda: HashTable(),
        "hash?": lambda x: isinstance(x, HashTable),
        "hash-set!": _hash_set,
        "hash-ref": _hash_ref,
        "hash-has-key?": lambda h, k: _freeze(k) in _ht("hash-has-key?", h),
        "hash-remove!": _hash_remove,
        "hash-count": lambda h: len(_ht("hash-count", h)),
        "hash-keys": lambda h: [k for k, _ in _ht("hash-keys", h).values()],
        "hash-values": lambda h: [v for _, v in _ht("hash-values", h).values()],
        "hash->list": lambda h: [[k, v] for k, v in _ht("hash->list", h).values()],
    }
