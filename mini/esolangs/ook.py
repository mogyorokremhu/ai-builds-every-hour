"""Ook! interpreter (a Brainfuck dialect). Usage: python ook.py [file]; runs a demo without args."""
import sys

MAP = {
    ("Ook.", "Ook?"): ">", ("Ook?", "Ook."): "<",
    ("Ook.", "Ook."): "+", ("Ook!", "Ook!"): "-",
    ("Ook!", "Ook."): ".", ("Ook.", "Ook!"): ",",
    ("Ook!", "Ook?"): "[", ("Ook?", "Ook!"): "]",
}
REV = {v: k for k, v in MAP.items()}


def to_bf(src: str) -> str:
    """Translate Ook! words (pairs) to Brainfuck."""
    words = src.split()
    if len(words) % 2:
        raise ValueError("Ook! programs need an even number of words")
    return "".join(MAP[(words[i], words[i + 1])] for i in range(0, len(words), 2))


def from_bf(bf: str) -> str:
    """Translate Brainfuck to Ook!."""
    return " ".join(" ".join(REV[c]) for c in bf if c in REV)


def run_bf(code: str, inp: str = "") -> str:
    jump, stack = {}, []
    for i, c in enumerate(code):
        if c == "[":
            stack.append(i)
        elif c == "]":
            j = stack.pop()
            jump[i], jump[j] = j, i
    tape, p, pc, out, ip = [0] * 30000, 0, 0, [], 0
    while pc < len(code):
        c = code[pc]
        if c == ">": p += 1
        elif c == "<": p -= 1
        elif c == "+": tape[p] = (tape[p] + 1) % 256
        elif c == "-": tape[p] = (tape[p] - 1) % 256
        elif c == ".": out.append(chr(tape[p]))
        elif c == ",":
            tape[p] = ord(inp[ip]) if ip < len(inp) else 0
            ip += 1
        elif c == "[" and tape[p] == 0: pc = jump[pc]
        elif c == "]" and tape[p] != 0: pc = jump[pc]
        pc += 1
    return "".join(out)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        print(run_bf(to_bf(open(sys.argv[1]).read())))
    else:
        hello = "++++++++[>+++++++++<-]>.+++++++++++++++++++++++++++++.+++++++..+++."
        ook = from_bf(hello)
        print(ook[:60], "...")
        assert to_bf(ook) == hello
        print(run_bf(to_bf(ook)))
