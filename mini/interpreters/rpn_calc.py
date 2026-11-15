"""Reverse Polish notation calculator. Usage: python rpn_calc.py "3 4 + 2 *" """
import math
import sys

OPS = {"+": lambda a, b: a + b, "-": lambda a, b: a - b, "*": lambda a, b: a * b,
       "/": lambda a, b: a / b, "^": lambda a, b: a ** b}
FUNCS = {"sqrt": math.sqrt, "neg": lambda a: -a, "abs": abs}


def evaluate(expr: str) -> float:
    st: list[float] = []
    for tok in expr.split():
        if tok in OPS:
            b, a = st.pop(), st.pop()
            st.append(OPS[tok](a, b))
        elif tok in FUNCS:
            st.append(FUNCS[tok](st.pop()))
        elif tok == "dup":
            st.append(st[-1])
        elif tok == "swap":
            st[-1], st[-2] = st[-2], st[-1]
        else:
            st.append(float(tok))
    if len(st) != 1:
        raise ValueError(f"stack has {len(st)} items: {st}")
    return st[0]


if __name__ == "__main__":
    print(evaluate(sys.argv[1] if len(sys.argv) > 1 else "3 4 + 2 *"))
