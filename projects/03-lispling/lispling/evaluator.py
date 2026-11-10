"""The evaluator, with tail-call optimisation."""
from __future__ import annotations
from pathlib import Path
from . import builtins, forms, higher, stdlib, vectors
from .reader import parse
from .pairs import Pair
from .types import Env, Lambda, LispError, Macro, Symbol, bind_params, sym, to_string

S = sym


PRELUDE = Path(__file__).with_name("prelude.lisp")


def global_env(out=print, prelude=True) -> Env:
    env = Env()
    builtins.install(env, out)
    env.update(higher.make(evaluate))
    env.update(stdlib.make())
    env.update(vectors.make())
    if prelude:
        for e in parse(PRELUDE.read_text()):
            evaluate(e, env)
    return env


def _truthy(x) -> bool:
    return x is not False


def _lookup_macro(name, env):
    e = env
    while e is not None:
        if name in e:
            return e[name] if isinstance(e[name], Macro) else None
        e = e.parent
    return None


def expand_macro(m: Macro, args):
    """Run the macro body on the unevaluated args and return the new form."""
    if len(args) != len(m.params):
        raise LispError(f"macro {m.name} expects {len(m.params)} args, got {len(args)}")
    menv = Env(m.env)
    menv.update(zip(m.params, args))
    r = []
    for e in m.body:
        r = evaluate(e, menv)
    return r


def evaluate(x, env: Env):
    while True:
        if isinstance(x, Symbol):
            return env.find(x)[x]
        if not isinstance(x, list):
            return x
        if not x:
            raise LispError("cannot evaluate empty list ()")
        head = x[0]
        if head == "quote":
            return x[1]
        if head == "if":
            if len(x) < 3:
                raise LispError("if needs a test and a branch")
            if _truthy(evaluate(x[1], env)):
                x = x[2]
            elif len(x) > 3:
                x = x[3]
            else:
                return []
            continue
        if head == "define":
            target = x[1]
            if isinstance(target, Pair):  # (define (f a . rest) body...)
                name = target.car
                env[name] = Lambda(target.cdr, x[2:], env, name)
            elif isinstance(target, list):  # (define (f a b) body...)
                name = target[0]
                env[name] = Lambda(target[1:], x[2:], env, name)
            else:
                val = evaluate(x[2], env)
                if isinstance(val, Lambda) and not val.name:
                    val.name = target
                env[target] = val
            return []
        if head == "define-macro":
            if len(x) < 3 or not isinstance(x[1], list) or not x[1]:
                raise LispError("define-macro needs (name params...) and a body")
            env[x[1][0]] = Macro(x[1][1:], x[2:], env, x[1][0])
            return []
        if head == "set!":
            env.find(x[1])[x[1]] = evaluate(x[2], env)
            return []
        if head == "lambda":
            return Lambda(x[1], x[2:], env)
        if head == "begin":
            for e in x[1:-1]:
                evaluate(e, env)
            x = x[-1]
            continue
        if isinstance(head, Symbol) and head in forms.EXPANDERS:
            x = forms.EXPANDERS[head](x)
            continue
        if head == "let" and len(x) > 1 and isinstance(x[1], Symbol):
            x = forms.expand_named_let(x)
            continue
        if head == "let":
            inner = Env(env)
            for name, e in x[1]:
                inner[name] = evaluate(e, env)
            for e in x[2:-1]:
                evaluate(e, inner)
            x, env = x[-1], inner
            continue
        if head == "cond":
            for clause in x[1:]:
                if clause[0] == "else" or _truthy(evaluate(clause[0], env)):
                    for e in clause[1:-1]:
                        evaluate(e, env)
                    x = clause[-1]
                    break
            else:
                return []
            continue
        if head == "and":
            if len(x) == 1:
                return True
            for e in x[1:-1]:
                if not _truthy(evaluate(e, env)):
                    return False
            x = x[-1]  # last operand is in tail position
            continue
        if head == "or":
            if len(x) == 1:
                return False
            for e in x[1:-1]:
                r = evaluate(e, env)
                if _truthy(r):
                    return r
            x = x[-1]
            continue
        if isinstance(head, Symbol):
            m = _lookup_macro(head, env)
            if m is not None:
                x = expand_macro(m, x[1:])
                continue
        # procedure call
        f = evaluate(head, env)
        args = [evaluate(a, env) for a in x[1:]]
        if isinstance(f, Lambda):
            env = Env(f.env)
            bind_params(env, f.params, f.rest, args, f.name)
            for e in f.body[:-1]:
                evaluate(e, env)
            x = f.body[-1]
            continue
        if callable(f):
            try:
                return f(*args)
            except TypeError as e:
                raise LispError(f"bad call: {e}") from None
        raise LispError(f"not a procedure: {to_string(f)}")


def run(src: str, env: Env | None = None):
    """Evaluate every expression in src; return the last result."""
    env = env if env is not None else global_env()
    result = []
    for e in parse(src):
        result = evaluate(e, env)
    return result
