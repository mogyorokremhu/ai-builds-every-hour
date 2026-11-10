"""Higher-order builtins: map, filter, reduce, apply, for-each, plus error/try."""
from __future__ import annotations
from .types import Env, Lambda, LispError, bind_params, to_string


def make(evaluate):
    def call(f, args):
        if isinstance(f, Lambda):
            env = Env(f.env)
            bind_params(env, f.params, f.rest, args, f.name)
            r = []
            for e in f.body:
                r = evaluate(e, env)
            return r
        if callable(f):
            return f(*args)
        raise LispError(f"not a procedure: {to_string(f)}")

    def _lists(name, ls):
        for l in ls:
            if not isinstance(l, list):
                raise LispError(f"{name}: expected list, got {to_string(l)}")

    def map_(f, *ls):
        _lists("map", ls)
        return [call(f, list(a)) for a in zip(*ls)]

    def for_each(f, *ls):
        _lists("for-each", ls)
        for a in zip(*ls):
            call(f, list(a))
        return []

    def filter_(f, l):
        _lists("filter", [l])
        return [x for x in l if call(f, [x]) is not False]

    def reduce_(f, init, l):
        _lists("reduce", [l])
        acc = init
        for x in l:
            acc = call(f, [acc, x])
        return acc

    def apply_(f, *args):
        if not args or not isinstance(args[-1], list):
            raise LispError("apply: last argument must be a list")
        return call(f, list(args[:-1]) + args[-1])

    def error_(msg, *irritants):
        text = msg if isinstance(msg, str) else to_string(msg)
        if irritants:
            text += ": " + " ".join(to_string(i) for i in irritants)
        raise LispError(text)

    def try_(thunk, handler):
        """(try thunk handler): call thunk; on a LispError call handler with the message."""
        try:
            return call(thunk, [])
        except LispError as e:
            return call(handler, [str(e)])

    return {"error": error_, "try": try_, "map": map_, "for-each": for_each, "filter": filter_,
            "reduce": reduce_, "fold": reduce_, "apply": apply_}
