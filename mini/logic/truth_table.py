"""Print the truth table of a boolean expression (and, or, not, ^, ->, parentheses)."""
import itertools
import re
import sys


def variables(expr: str) -> list[str]:
    """Return sorted variable names (single identifiers that aren't keywords)."""
    return sorted(set(re.findall(r"[A-Za-z_]\w*", expr)) - {"and", "or", "not", "True", "False"})


def evaluate(expr: str, env: dict[str, bool]) -> bool:
    """Evaluate expr; '->' is implication, '^' is xor."""
    # a -> b  ==  (not a) or b  (right-assoc handled by repeated rewrite of the last arrow)
    parts = expr.split("->")
    py = parts[-1]
    for left in reversed(parts[:-1]):
        py = f"(not ({left})) or ({py})"
    return bool(eval(py, {"__builtins__": {}}, dict(env)))


def table(expr: str) -> list[tuple[dict[str, bool], bool]]:
    vs = variables(expr)
    return [(dict(zip(vs, vals)), evaluate(expr, dict(zip(vs, vals))))
            for vals in itertools.product([False, True], repeat=len(vs))]


def main() -> None:
    expr = " ".join(sys.argv[1:]) or "(a and b) or not c"
    rows = table(expr)
    vs = variables(expr)
    print(" ".join(vs), "|", expr)
    for env, out in rows:
        print(" ".join("1" if env[v] else "0" for v in vs), "|", int(out))
    if all(o for _, o in rows):
        print("tautology")
    elif not any(o for _, o in rows):
        print("contradiction")
    assert table("a -> b")[2][1] is False  # a=1,b=0


if __name__ == "__main__":
    main()
