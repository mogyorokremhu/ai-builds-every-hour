"""Tiny BASIC: LET, PRINT, IF..THEN, GOTO, END with line numbers. Runs a countdown/sum demo."""

PROGRAM = """
10 LET N = 5
20 LET S = 0
30 LET S = S + N
40 PRINT N, S
50 LET N = N - 1
60 IF N > 0 THEN 30
70 PRINT S
80 END
"""


def run(src: str, max_steps: int = 10000) -> list:
    lines = {}
    for ln in src.strip().splitlines():
        num, _, rest = ln.strip().partition(" ")
        lines[int(num)] = rest
    order, env, out = sorted(lines), {}, []
    pc = 0
    for _ in range(max_steps):
        if pc >= len(order):
            break
        stmt = lines[order[pc]]
        kw, _, rest = stmt.partition(" ")
        pc += 1
        if kw == "LET":
            name, _, e = rest.partition("=")
            env[name.strip()] = eval(e, {}, env)
        elif kw == "PRINT":
            out.append(" ".join(str(eval(p, {}, env)) for p in rest.split(",")))
        elif kw == "GOTO":
            pc = order.index(int(rest))
        elif kw == "IF":
            cond, _, target = rest.partition(" THEN ")
            if eval(cond.replace("<>", "!="), {}, env):
                pc = order.index(int(target))
        elif kw == "END":
            break
    return out


if __name__ == "__main__":
    print("\n".join(run(PROGRAM)))
