"""Shunting-yard: infix expression -> RPN -> value (+ - * / ^ and parentheses)."""
import re

PREC = {"+": (1, "L"), "-": (1, "L"), "*": (2, "L"), "/": (2, "L"), "^": (3, "R")}


def to_rpn(expr: str) -> list[str]:
    out, ops = [], []
    for tok in re.findall(r"\d+\.?\d*|[-+*/^()]", expr):
        if tok in PREC:
            p, assoc = PREC[tok]
            while ops and ops[-1] in PREC and (
                PREC[ops[-1]][0] > p or (PREC[ops[-1]][0] == p and assoc == "L")
            ):
                out.append(ops.pop())
            ops.append(tok)
        elif tok == "(":
            ops.append(tok)
        elif tok == ")":
            while ops and ops[-1] != "(":
                out.append(ops.pop())
            if not ops:
                raise ValueError("mismatched parentheses")
            ops.pop()
        else:
            out.append(tok)
    while ops:
        if ops[-1] == "(":
            raise ValueError("mismatched parentheses")
        out.append(ops.pop())
    return out


def eval_rpn(rpn: list[str]) -> float:
    st: list[float] = []
    for t in rpn:
        if t in PREC:
            b, a = st.pop(), st.pop()
            st.append({"+": a + b, "-": a - b, "*": a * b, "/": a / b, "^": a ** b}[t])
        else:
            st.append(float(t))
    return st[0]


if __name__ == "__main__":
    for e in ["1 + 2 * 3", "(1 + 2) * 3", "2 ^ 3 ^ 2", "10 / 4 - 1"]:
        r = to_rpn(e)
        print(f"{e:14} -> {' '.join(r):14} = {eval_rpn(r)}")
    assert eval_rpn(to_rpn("2 ^ 3 ^ 2")) == 512
