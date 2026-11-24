"""A small DPLL SAT solver over CNF given as lists of ints (negative = negated)."""
from __future__ import annotations


def dpll(clauses: list[list[int]], assign: dict[int, bool] | None = None) -> dict[int, bool] | None:
    """Return a satisfying assignment or None."""
    assign = dict(assign or {})
    clauses = [list(c) for c in clauses]
    while True:  # unit propagation
        units = [c[0] for c in clauses if len(c) == 1]
        if not units:
            break
        lit = units[0]
        assign[abs(lit)] = lit > 0
        new = []
        for c in clauses:
            if lit in c:
                continue
            c2 = [x for x in c if x != -lit]
            if not c2:
                return None
            new.append(c2)
        clauses = new
    if not clauses:
        return assign
    lit = clauses[0][0]
    for choice in (lit, -lit):
        res = dpll(clauses + [[choice]], assign)
        if res is not None:
            return res
    return None


def check(clauses: list[list[int]], model: dict[int, bool]) -> bool:
    return all(any(model.get(abs(l), False) == (l > 0) for l in c) for c in clauses)


def pigeonhole(n: int) -> list[list[int]]:
    """n+1 pigeons into n holes: unsatisfiable."""
    v = lambda p, h: p * n + h + 1
    cl = [[v(p, h) for h in range(n)] for p in range(n + 1)]
    for h in range(n):
        for p in range(n + 1):
            for q in range(p + 1, n + 1):
                cl.append([-v(p, h), -v(q, h)])
    return cl


if __name__ == "__main__":
    f = [[1, 2], [-1, 3], [-2, -3], [2, 3]]
    m = dpll(f)
    print("model:", m)
    assert m is not None and check(f, m)
    assert dpll(pigeonhole(3)) is None
    print("pigeonhole(3) unsat: ok")
