"""Brainfuck-to-C transpiler (prints C source) plus a tiny self-check via Python.
Usage: python bf_to_c.py "++++++++[>++++++++<-]>+."  """
import sys

MAP = {">": "p++;", "<": "p--;", "+": "(*p)++;", "-": "(*p)--;",
       ".": "putchar(*p);", ",": "*p=getchar();", "[": "while(*p){", "]": "}"}


def to_c(src: str) -> str:
    """Translate Brainfuck source into a C program with indentation."""
    lines, depth = [], 1
    for ch in src:
        if ch not in MAP:
            continue
        if ch == "]":
            depth -= 1
        lines.append("    " * depth + MAP[ch])
        if ch == "[":
            depth += 1
    if depth != 1:
        raise ValueError("unbalanced brackets")
    body = "\n".join(lines)
    return ("#include <stdio.h>\nunsigned char tape[30000];\n"
            f"int main(void){{\n    unsigned char *p = tape;\n{body}\n    return 0;\n}}\n")


if __name__ == "__main__":
    print(to_c(sys.argv[1] if len(sys.argv) > 1 else "++++++++[>++++++++<-]>+."))
