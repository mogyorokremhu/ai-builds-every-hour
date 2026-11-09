"""Derived special forms, rewritten into core forms (keeps tail calls intact).

Each expander takes the whole form and returns a new expression that the
evaluator then continues with, so `do`, named `let` etc. are tail-safe.
"""
from __future__ import annotations
from .types import LispError, sym

S = sym


def _list(*a):
    return list(a)


def _append(*a):
    return [i for l in a for i in l]


def expand_let_star(x):
    """(let* ((a 1) (b a)) body...) -> nested lets."""
    if len(x) < 3 or not isinstance(x[1], list):
        raise LispError("let* needs bindings and a body")
    binds, body = x[1], x[2:]
    if not binds:
        return [S("let"), [], *body]
    out = [S("let"), [binds[-1]], *body]
    for b in reversed(binds[:-1]):
        out = [S("let"), [b], out]
    return out


def expand_letrec(x):
    """(letrec ((f e)...) body...) -> (let () (define f e)... body...)."""
    if len(x) < 3 or not isinstance(x[1], list):
        raise LispError("letrec needs bindings and a body")
    return [S("let"), [], *[[S("define"), n, e] for n, e in x[1]], *x[2:]]


def expand_named_let(x):
    """(let loop ((v init)...) body...) -> ((letrec ((loop (lambda ...))) loop) init...)."""
    if len(x) < 4:
        raise LispError("named let needs a name, bindings and a body")
    name, binds, body = x[1], x[2], x[3:]
    params = [b[0] for b in binds]
    inits = [b[1] for b in binds]
    fn = [S("lambda"), params, *body]
    return [[S("letrec"), [[name, fn]], name], *inits]


def expand_do(x):
    """(do ((v init step)...) (test result...) body...)."""
    if len(x) < 3 or not isinstance(x[2], list) or not x[2]:
        raise LispError("do needs bindings and a (test result...) clause")
    loop = S("%do-loop")
    specs = x[1]
    for s in specs:
        if not isinstance(s, list) or len(s) not in (2, 3):
            raise LispError("do binding must be (var init [step])")
    binds = [[s[0], s[1]] for s in specs]
    steps = [s[2] if len(s) == 3 else s[0] for s in specs]
    test, results = x[2][0], x[2][1:]
    done = [S("begin"), *results] if results else [S("quote"), []]
    again = [S("begin"), *x[3:], [loop, *steps]]
    return [S("let"), loop, binds, [S("if"), test, done, again]]


def expand_quasiquote(x):
    """Expand `template (one level; unquote and unquote-splicing)."""
    if len(x) != 2:
        raise LispError("quasiquote takes one template")
    return _qq(x[1])


def _qq(t):
    if not isinstance(t, list):
        return [S("quote"), t]
    if not t:
        return [S("quote"), []]
    if t[0] == "unquote":
        return t[1]
    if t[0] == "unquote-splicing":
        raise LispError("unquote-splicing outside a list")
    parts = []
    for e in t:
        if isinstance(e, list) and e and e[0] == "unquote-splicing":
            parts.append(e[1])
        else:
            parts.append([_list, _qq(e)])
    return [_append, *parts]


_case_n = 0


def expand_case(x):
    """(case key ((d ...) body...) ... (else body...)) -> let + cond with equal?."""
    global _case_n
    if len(x) < 2:
        raise LispError("case needs a key expression")
    _case_n += 1
    k = S(f"%case-key{_case_n}")
    clauses = []
    for c in x[2:]:
        if not isinstance(c, list) or len(c) < 2:
            raise LispError("case clause needs data and a body")
        if c[0] == S("else"):
            clauses.append([S("else"), *c[1:]])
        elif isinstance(c[0], list):
            test = [S("or"), *[[S("equal?"), k, [S("quote"), d]] for d in c[0]]]
            clauses.append([test, *c[1:]])
        else:
            raise LispError("case clause data must be a list")
    return [S("let"), [[k, x[1]]], [S("cond"), *clauses]]


def expand_when(x):
    """(when test body...) -> (if test (begin body...) '())."""
    if len(x) < 3:
        raise LispError("when needs a test and a body")
    return [S("if"), x[1], [S("begin"), *x[2:]], [S("quote"), []]]


def expand_unless(x):
    """(unless test body...) -> (if test '() (begin body...))."""
    if len(x) < 3:
        raise LispError("unless needs a test and a body")
    return [S("if"), x[1], [S("quote"), []], [S("begin"), *x[2:]]]


def expand_assert(x):
    """(assert expr) -> error naming the failed expression."""
    if len(x) != 2:
        raise LispError("assert takes exactly one expression")
    return [S("if"), x[1], True, [S("error"), "assertion failed", [S("quote"), x[1]]]]


def expand_define_record_type(x):
    """(define-record-type name (ctor field...) pred (field getter [setter])...).

    Records are tagged vectors: #(name v1 v2 ...). Expands to a begin of defines.
    """
    if len(x) < 4 or not isinstance(x[2], list) or not x[2]:
        raise LispError("define-record-type needs a name, a constructor spec and a predicate")
    name, (ctor, *cfields), pred = x[1], x[2], x[3]
    specs = x[4:]
    fields = []
    for sp in specs:
        if not isinstance(sp, list) or len(sp) not in (2, 3):
            raise LispError("define-record-type field spec is (field getter [setter])")
        fields.append(sp[0])
    for f in cfields:
        if f not in fields:
            raise LispError(f"define-record-type: constructor field {f} is not a declared field")
    tag = [S("quote"), name]
    o, v = S("%rec"), S("%val")
    out = [S("begin")]
    # fields not in the constructor default to 0
    args = [(f if f in cfields else 0) for f in fields]
    out.append([S("define"), [ctor, *cfields], [S("vector"), tag, *args]])
    out.append([S("define"), [pred, o],
                [S("and"), [S("vector?"), o], [S(">"), [S("vector-length"), o], 0],
                 [S("equal?"), [S("vector-ref"), o, 0], tag]]])
    for i, sp in enumerate(specs, start=1):
        getter = [S("define"), [sp[1], o],
                  [S("if"), [pred, o], [S("vector-ref"), o, i],
                   [S("error"), f"{sp[1]}: not a {name}", o]]]
        out.append(getter)
        if len(sp) == 3:
            out.append([S("define"), [sp[2], o, v],
                        [S("if"), [pred, o], [S("vector-set!"), o, i, v],
                         [S("error"), f"{sp[2]}: not a {name}", o]]])
    return out


EXPANDERS = {
    "define-record-type": expand_define_record_type,
    "when": expand_when,
    "unless": expand_unless,
    "assert": expand_assert,
    "case": expand_case,
    "let*": expand_let_star,
    "letrec": expand_letrec,
    "do": expand_do,
    "quasiquote": expand_quasiquote,
}
