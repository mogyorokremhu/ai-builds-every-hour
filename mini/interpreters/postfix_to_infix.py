"""Convert postfix (RPN) expressions to fully/minimally parenthesised infix.
Usage: python postfix_to_infix.py "3 4 + 5 *"  """
import sys

PREC = {"+": 1, "-": 1, "*": 2, "/": 2, "^": 3}
RIGHT = {"^"}


def convert(expr: str) -> str:
    """Return minimal-parenthesis infix for a postfix expression."""
    st: list[tuple[str, int]] = []
    for t in expr.split():
        if t in PREC:
            if len(st) < 2:
                raise ValueError("stack underflow")
            (b, pb), (a, pa) = st.pop(), st.pop()
            p = PREC[t]
            if pa < p or (pa == p and t in RIGHT):
                a = f"({a})"
            if pb < p or (pb == p and t not in RIGHT):
                b = f"({b})"
            st.append((f"{a} {t} {b}", p))
        else:
            st.append((t, 9))
    if len(st) != 1:
        raise ValueError("malformed expression")
    return st[0][0]


if __name__ == "__main__":
    for e in (sys.argv[1:] or ["3 4 + 5 *", "1 2 3 * +", "2 3 ^ 2 ^", "8 3 2 - -"]):
        print(f"{e}  =>  {convert(e)}")
