"""Minsky register machine: INC r / DECJZ r target / HALT, with a text assembler."""


def assemble(src: str):
    prog = []
    for line in src.strip().splitlines():
        parts = line.split("#")[0].split()
        if parts:
            prog.append(parts)
    return prog


def run(prog, regs, max_steps=100000):
    pc, steps = 0, 0
    while 0 <= pc < len(prog) and steps < max_steps:
        ins = prog[pc]
        steps += 1
        if ins[0] == "INC":
            regs[ins[1]] = regs.get(ins[1], 0) + 1
            pc += 1
        elif ins[0] == "DECJZ":
            if regs.get(ins[1], 0) == 0:
                pc = int(ins[2])
            else:
                regs[ins[1]] -= 1
                pc += 1
        elif ins[0] == "JMP":
            pc = int(ins[1])
        elif ins[0] == "HALT":
            break
    return regs, steps


ADD = """
DECJZ b 4    # 0: while b>0
INC a        # 1
JMP 0        # 2
HALT         # 3 (unused)
HALT         # 4
"""

if __name__ == "__main__":
    regs, steps = run(assemble(ADD), {"a": 3, "b": 4})
    print("3 + 4 =", regs["a"], f"({steps} steps)")
