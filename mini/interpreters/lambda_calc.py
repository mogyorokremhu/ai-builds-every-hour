"""Untyped lambda calculus: parser and normal-order reducer. Syntax: \\x.body, application by juxtaposition."""
import itertools

_fresh = itertools.count()


def parse(s: str):
    toks = s.replace("\\", " \\ ").replace(".", " . ").replace("(", " ( ").replace(")", " ) ").split()
    pos = 0

    def term():
        nonlocal pos
        if toks[pos] == "\\":
            v = toks[pos + 1]
            pos += 3
            return ("lam", v, term())
        t = atom()
        while pos < len(toks) and toks[pos] not in (")",):
            t = ("app", t, atom()) if toks[pos] != "\\" else ("app", t, term())
        return t

    def atom():
        nonlocal pos
        if toks[pos] == "(":
            pos += 1
            t = term()
            pos += 1
            return t
        pos += 1
        return ("var", toks[pos - 1])

    return term()


def free(t):
    if t[0] == "var":
        return {t[1]}
    if t[0] == "lam":
        return free(t[2]) - {t[1]}
    return free(t[1]) | free(t[2])


def subst(t, v, r):
    if t[0] == "var":
        return r if t[1] == v else t
    if t[0] == "app":
        return ("app", subst(t[1], v, r), subst(t[2], v, r))
    if t[1] == v:
        return t
    if t[1] in free(r):
        n = f"{t[1]}{next(_fresh)}"
        return ("lam", n, subst(subst(t[2], t[1], ("var", n)), v, r))
    return ("lam", t[1], subst(t[2], v, r))


def step(t):
    if t[0] == "app":
        f = t[1]
        if f[0] == "lam":
            return subst(f[2], f[1], t[2])
        s = step(f)
        if s is not None:
            return ("app", s, t[2])
        s = step(t[2])
        return None if s is None else ("app", f, s)
    if t[0] == "lam":
        s = step(t[2])
        return None if s is None else ("lam", t[1], s)
    return None


def show(t):
    if t[0] == "var":
        return t[1]
    if t[0] == "lam":
        return f"\\{t[1]}.{show(t[2])}"
    a = show(t[2]) if t[2][0] == "var" else f"({show(t[2])})"
    f = show(t[1]) if t[1][0] != "lam" else f"({show(t[1])})"
    return f"{f} {a}"


def normalize(s: str, limit: int = 1000) -> str:
    t = parse(s)
    for _ in range(limit):
        n = step(t)
        if n is None:
            break
        t = n
    return show(t)


if __name__ == "__main__":
    print(normalize("(\\x.x) y"))
    print(normalize("(\\f.\\x.f (f x)) (\\a.a) z"))
    print(normalize("(\\x.\\y.x) a b"))
