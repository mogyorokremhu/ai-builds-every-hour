"""A safe command-line calculator with a hand-written Pratt parser.

Supports + - * / // % ** (right-assoc), unary minus, parentheses, variables
(`x = 3`), constants (pi, e, tau) and functions (sqrt, sin, cos, tan, log, exp,
abs, min, max, round, floor, ceil). No eval() anywhere.

    python calc.py "2 ** 3 ** 2"        -> 512
    python calc.py                      -> interactive REPL ("ans" holds the last result)
"""
from __future__ import annotations

import math
import re
import sys

TOKEN = re.compile(r"\s*(?:(\d+\.?\d*(?:[eE][-+]?\d+)?|\.\d+)|(\*\*|//|[-+*/%(),=])|([A-Za-z_]\w*))")

FUNCS = {
    "sqrt": math.sqrt, "sin": math.sin, "cos": math.cos, "tan": math.tan, "log": math.log,
    "exp": math.exp, "abs": abs, "min": min, "max": max, "round": round,
    "floor": math.floor, "ceil": math.ceil,
}
CONSTS = {"pi": math.pi, "e": math.e, "tau": math.tau}

# binding power: (left, right)
INFIX = {"+": (10, 11), "-": (10, 11), "*": (20, 21), "/": (20, 21), "//": (20, 21), "%": (20, 21),
         "**": (31, 30)}


def tokenize(src: str) -> list[tuple[str, str]]:
    out, pos = [], 0
    src = src.rstrip()
    while pos < len(src):
        m = TOKEN.match(src, pos)
        if not m:
            raise SyntaxError(f"unexpected character {src[pos]!r} at {pos}")
        num, op, name = m.groups()
        out.append(("num", num) if num else ("op", op) if op else ("name", name))
        pos = m.end()
    out.append(("end", ""))
    return out


class Parser:
    def __init__(self, src: str, env: dict[str, float]) -> None:
        self.toks = tokenize(src)
        self.i = 0
        self.env = env

    def peek(self) -> tuple[str, str]:
        return self.toks[self.i]

    def next(self) -> tuple[str, str]:
        t = self.toks[self.i]
        self.i += 1
        return t

    def expect(self, val: str) -> None:
        t = self.next()
        if t[1] != val:
            raise SyntaxError(f"expected {val!r}, got {t[1] or 'end of input'!r}")

    def statement(self) -> float:
        if self.peek()[0] == "name" and self.toks[self.i + 1][1] == "=":
            name = self.next()[1]
            self.next()
            val = self.expr(0)
            self.env[name] = val
        else:
            val = self.expr(0)
        if self.peek()[0] != "end":
            raise SyntaxError(f"unexpected {self.peek()[1]!r}")
        return val

    def expr(self, min_bp: int) -> float:
        left = self.prefix()
        while True:
            kind, op = self.peek()
            if kind != "op" or op not in INFIX:
                return left
            lbp, rbp = INFIX[op]
            if lbp < min_bp:
                return left
            self.next()
            right = self.expr(rbp)
            left = self.apply(op, left, right)

    def prefix(self) -> float:
        kind, val = self.next()
        if kind == "num":
            return float(val) if any(c in val for c in ".eE") else int(val)
        if val == "-":
            return -self.expr(25)  # binds tighter than * but looser than **
        if val == "+":
            return self.expr(25)
        if val == "(":
            v = self.expr(0)
            self.expect(")")
            return v
        if kind == "name":
            if self.peek()[1] == "(":
                self.next()
                args = []
                if self.peek()[1] != ")":
                    args.append(self.expr(0))
                    while self.peek()[1] == ",":
                        self.next()
                        args.append(self.expr(0))
                self.expect(")")
                if val not in FUNCS:
                    raise NameError(f"unknown function {val}")
                return FUNCS[val](*args)
            if val in self.env:
                return self.env[val]
            if val in CONSTS:
                return CONSTS[val]
            raise NameError(f"unknown name {val}")
        raise SyntaxError(f"unexpected {val or 'end of input'!r}")

    @staticmethod
    def apply(op: str, a: float, b: float) -> float:
        if op == "+":
            return a + b
        if op == "-":
            return a - b
        if op == "*":
            return a * b
        if op == "/":
            return a / b
        if op == "//":
            return a // b
        if op == "%":
            return a % b
        return a ** b


def evaluate(src: str, env: dict[str, float] | None = None) -> float:
    return Parser(src, env if env is not None else {}).statement()


def fmt(v: float) -> str:
    if isinstance(v, float) and v.is_integer() and abs(v) < 1e15:
        return str(int(v))
    return repr(v)


def main() -> None:
    if len(sys.argv) > 1:
        print(fmt(evaluate(" ".join(sys.argv[1:]))))
        return
    env: dict[str, float] = {}
    print("calc — empty line or Ctrl-D to quit")
    while True:
        try:
            line = input("> ")
        except EOFError:
            break
        if not line.strip():
            break
        try:
            env["ans"] = evaluate(line, env)
            print(fmt(env["ans"]))
        except (SyntaxError, NameError, ZeroDivisionError, ValueError, TypeError, OverflowError) as exc:
            print(f"error: {exc}")


if __name__ == "__main__":
    main()
