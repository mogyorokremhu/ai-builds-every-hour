"""Infix calculator: shunting-yard to RPN, then evaluation. Supports + - * / ^ and parentheses."""
import re

PREC = {"+": (1, "L"), "-": (1, "L"), "*": (2, "L"), "/": (2, "L"), "^": (3, "R")}


def to_rpn(expr: str) -> list:
    out, ops = [], []
    for tok in re.findall(r"\d+\.?\d*|[-+*/^()]", expr):
        if tok[0].isdigit():
            out.append(float(tok))
        elif tok == "(":
            ops.append(tok)
        elif tok == ")":
            while ops and ops[-1] != "(":
                out.append(ops.pop())
            ops.pop()
        else:
            p, a = PREC[tok]
            while ops and ops[-1] in PREC and (PREC[ops[-1]][0] > p or (PREC[ops[-1]][0] == p and a == "L")):
                out.append(ops.pop())
            ops.append(tok)
    return out + ops[::-1]


def evaluate(expr: str) -> float:
    st = []
    for t in to_rpn(expr):
        if isinstance(t, float):
            st.append(t)
        else:
            b, a = st.pop(), st.pop()
            st.append({"+": a + b, "-": a - b, "*": a * b, "/": a / b if b else float("nan"), "^": a ** b}[t])
    return st[0]


if __name__ == "__main__":
    for e in ["1 + 2 * 3", "(1 + 2) * 3", "2 ^ 3 ^ 2", "10 / 4 - 1"]:
        print(f"{e} = {evaluate(e):g}")
