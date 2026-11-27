"""Compile Brainfuck to C source (run-length folded). Usage: python bf_to_c.py [file]; prints C code."""
import sys

DEMO = "++++++++[>++++[>++>+++>+++>+<<<<-]>+>+>->>+[<]<-]>>.>---.+++++++..+++.>>.<-.<.+++.------.--------.>>+."


def compile_bf(code: str) -> str:
    out = ["#include <stdio.h>", "int main(void){", "  unsigned char t[30000]={0}, *p=t;"]
    ind, i, code = 1, 0, [c for c in code if c in "+-<>[].,"]
    while i < len(code):
        c = code[i]
        if c in "+-<>":
            j = i
            while j < len(code) and code[j] == c:
                j += 1
            n = j - i
            stmt = {"+": f"*p+={n};", "-": f"*p-={n};", ">": f"p+={n};", "<": f"p-={n};"}[c]
            out.append("  " * ind + stmt)
            i = j
            continue
        if c == "[":
            out.append("  " * ind + "while(*p){"); ind += 1
        elif c == "]":
            ind -= 1; out.append("  " * ind + "}")
        elif c == ".":
            out.append("  " * ind + "putchar(*p);")
        else:
            out.append("  " * ind + "*p=getchar();")
        i += 1
    out += ["  return 0;", "}"]
    return "\n".join(out)


if __name__ == "__main__":
    print(compile_bf(open(sys.argv[1]).read() if len(sys.argv) > 1 else DEMO))
