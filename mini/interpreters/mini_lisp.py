"""A tiny Scheme-like interpreter: define, lambda, if, quote, arithmetic."""
import math
import operator as op


def tokenize(src):
    return src.replace("(", " ( ").replace(")", " ) ").split()


def parse(tokens):
    tok = tokens.pop(0)
    if tok == "(":
        out = []
        while tokens[0] != ")":
            out.append(parse(tokens))
        tokens.pop(0)
        return out
    try:
        return int(tok)
    except ValueError:
        try:
            return float(tok)
        except ValueError:
            return tok


def global_env():
    env = {"+": lambda *a: sum(a), "-": op.sub, "*": lambda *a: math.prod(a),
           "/": op.truediv, "<": op.lt, ">": op.gt, "=": op.eq, "<=": op.le,
           "car": lambda l: l[0], "cdr": lambda l: l[1:], "cons": lambda a, l: [a] + l,
           "list": lambda *a: list(a), "null?": lambda l: l == []}
    return env


def evaluate(x, env):
    if isinstance(x, str):
        return env[x]
    if not isinstance(x, list):
        return x
    head = x[0]
    if head == "quote":
        return x[1]
    if head == "if":
        return evaluate(x[2] if evaluate(x[1], env) else x[3], env)
    if head == "define":
        env[x[1]] = evaluate(x[2], env)
        return None
    if head == "lambda":
        params, body = x[1], x[2]
        return lambda *args: evaluate(body, {**env, **dict(zip(params, args))})
    fn = evaluate(head, env)
    return fn(*[evaluate(a, env) for a in x[1:]])


def run(src, env=None):
    env = env if env is not None else global_env()
    tokens, result = tokenize(src), None
    while tokens:
        result = evaluate(parse(tokens), env)
    return result


if __name__ == "__main__":
    env = global_env()
    run("(define fact (lambda (n) (if (< n 2) 1 (* n (fact (- n 1))))))", env)
    print("fact(10) =", run("(fact 10)", env))
    run("(define map1 (lambda (f l) (if (null? l) (quote ()) (cons (f (car l)) (map1 f (cdr l))))))", env)
    print(run("(map1 (lambda (x) (* x x)) (list 1 2 3 4))", env))
