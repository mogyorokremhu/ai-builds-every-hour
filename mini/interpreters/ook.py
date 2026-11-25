"""Ook! interpreter: Brainfuck with an orangutan vocabulary."""

MAP = {("Ook.", "Ook?"): ">", ("Ook?", "Ook."): "<", ("Ook.", "Ook."): "+",
       ("Ook!", "Ook!"): "-", ("Ook!", "Ook."): ".", ("Ook.", "Ook!"): ",",
       ("Ook!", "Ook?"): "[", ("Ook?", "Ook!"): "]"}


def ook_to_bf(src: str) -> str:
    words = src.split()
    if len(words) % 2:
        raise ValueError("Ook! programs need an even number of words")
    return "".join(MAP[(words[i], words[i + 1])] for i in range(0, len(words), 2))


def bf_to_ook(bf: str) -> str:
    rev = {v: k for k, v in MAP.items()}
    return " ".join(" ".join(rev[c]) for c in bf if c in rev)


def run_bf(code: str, inp: str = "") -> str:
    jump, stack = {}, []
    for i, c in enumerate(code):
        if c == "[":
            stack.append(i)
        elif c == "]":
            j = stack.pop()
            jump[i], jump[j] = j, i
    tape, ptr, pc, out, inp = [0] * 30000, 0, 0, [], list(inp)
    while pc < len(code):
        c = code[pc]
        if c == ">": ptr += 1
        elif c == "<": ptr -= 1
        elif c == "+": tape[ptr] = (tape[ptr] + 1) % 256
        elif c == "-": tape[ptr] = (tape[ptr] - 1) % 256
        elif c == ".": out.append(chr(tape[ptr]))
        elif c == ",": tape[ptr] = ord(inp.pop(0)) if inp else 0
        elif c == "[" and tape[ptr] == 0: pc = jump[pc]
        elif c == "]" and tape[ptr] != 0: pc = jump[pc]
        pc += 1
    return "".join(out)


if __name__ == "__main__":
    bf = "++++++++[>++++++++<-]>+."  # prints 'A'
    ook = bf_to_ook(bf)
    print(ook[:60], "...")
    print(run_bf(ook_to_bf(ook)))
