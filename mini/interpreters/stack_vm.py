"""A small stack VM with labels, jumps and a text assembler; computes 5! by default."""

PROGRAM = """
push 5
store n
push 1
store acc
loop:
load n
jz end
load acc
load n
mul
store acc
load n
push 1
sub
store n
jmp loop
end:
load acc
print
"""


def assemble(src: str):
    """Turn source text into (instructions, labels)."""
    code, labels = [], {}
    for line in src.strip().splitlines():
        line = line.strip()
        if line.endswith(":"):
            labels[line[:-1]] = len(code)
        elif line:
            code.append(line.split())
    return code, labels


def run(src: str) -> list:
    """Execute the program; return printed values."""
    code, labels = assemble(src)
    stack, mem, out, pc = [], {}, [], 0
    ops = {"add": lambda a, b: a + b, "sub": lambda a, b: a - b, "mul": lambda a, b: a * b}
    while pc < len(code):
        op, *arg = code[pc]
        pc += 1
        if op == "push": stack.append(int(arg[0]))
        elif op in ops:
            b, a = stack.pop(), stack.pop()
            stack.append(ops[op](a, b))
        elif op == "load": stack.append(mem[arg[0]])
        elif op == "store": mem[arg[0]] = stack.pop()
        elif op == "jmp": pc = labels[arg[0]]
        elif op == "jz":
            if stack.pop() == 0: pc = labels[arg[0]]
        elif op == "print": out.append(stack.pop())
        else: raise ValueError(f"unknown op {op}")
    return out


if __name__ == "__main__":
    print(run(PROGRAM))
