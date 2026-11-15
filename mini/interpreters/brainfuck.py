"""Brainfuck interpreter. Usage: python brainfuck.py [program] (default: prints Hello World!)"""
import sys

HELLO = "++++++++[>++++[>++>+++>+++>+<<<<-]>+>+>->>+[<]<-]>>.>---.+++++++..+++.>>.<-.<.+++.------.--------.>>+."


def run(prog: str, inp: str = "", limit: int = 1_000_000) -> str:
    jump, stack = {}, []
    for i, c in enumerate(prog):
        if c == "[":
            stack.append(i)
        elif c == "]":
            j = stack.pop()
            jump[i], jump[j] = j, i
    tape, ptr, pc, out, ip, steps = [0] * 30000, 0, 0, [], 0, 0
    while pc < len(prog) and steps < limit:
        c = prog[pc]
        if c == ">": ptr += 1
        elif c == "<": ptr -= 1
        elif c == "+": tape[ptr] = (tape[ptr] + 1) % 256
        elif c == "-": tape[ptr] = (tape[ptr] - 1) % 256
        elif c == ".": out.append(chr(tape[ptr]))
        elif c == ",":
            tape[ptr] = ord(inp[ip]) if ip < len(inp) else 0
            ip += 1
        elif c == "[" and tape[ptr] == 0: pc = jump[pc]
        elif c == "]" and tape[ptr] != 0: pc = jump[pc]
        pc += 1
        steps += 1
    return "".join(out)


if __name__ == "__main__":
    print(run(sys.argv[1] if len(sys.argv) > 1 else HELLO))
