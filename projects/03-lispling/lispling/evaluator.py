"""The evaluator, with tail-call optimisation."""
from __future__ import annotations
from . import builtins
from .reader import parse
from .types import Env, Lambda, LispError, Symbol, sym, to_string

S = sym


def global_env(out=print) -> Env:
    env = Env()
    builtins.install(env, out)
    return env


def _truthy(x) -> bool:
    return x is not False


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
            if isinstance(target, list):  # (define (f a b) body...)
                name = target[0]
                env[name] = Lambda(target[1:], x[2:], env, name)
            else:
                val = evaluate(x[2], env)
                if isinstance(val, Lambda) and not val.name:
                    val.name = target
                env[target] = val
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
            r = True
            for e in x[1:]:
                r = evaluate(e, env)
                if not _truthy(r):
                    return False
            return r
        if head == "or":
            for e in x[1:]:
                r = evaluate(e, env)
                if _truthy(r):
                    return r
            return False
        # procedure call
        f = evaluate(head, env)
        args = [evaluate(a, env) for a in x[1:]]
        if isinstance(f, Lambda):
            if len(args) != len(f.params):
                raise LispError(f"{f.name or 'lambda'} expects {len(f.params)} args, got {len(args)}")
            env = Env(f.env)
            env.update(zip(f.params, args))
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
