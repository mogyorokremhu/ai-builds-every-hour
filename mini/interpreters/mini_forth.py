"""Tiny Forth: numbers, + - * / dup drop swap over . and : name ... ; definitions.
Usage: python mini_forth.py ": sq dup * ; 5 sq ."  """
import sys


def forth(src: str) -> str:
    words, st, out = {}, [], []
    toks = src.split()

    def exe(ts):
        i = 0
        while i < len(ts):
            t = ts[i]
            if t == ":":
                j = ts.index(";", i)
                words[ts[i + 1]] = ts[i + 2:j]
                i = j
            elif t in words:
                exe(words[t])
            elif t == "+": b, a = st.pop(), st.pop(); st.append(a + b)
            elif t == "-": b, a = st.pop(), st.pop(); st.append(a - b)
            elif t == "*": b, a = st.pop(), st.pop(); st.append(a * b)
            elif t == "/": b, a = st.pop(), st.pop(); st.append(a // b)
            elif t == "dup": st.append(st[-1])
            elif t == "drop": st.pop()
            elif t == "swap": st[-1], st[-2] = st[-2], st[-1]
            elif t == "over": st.append(st[-2])
            elif t == ".": out.append(str(st.pop()))
            else: st.append(int(t))
            i += 1

    exe(toks)
    return " ".join(out)


if __name__ == "__main__":
    print(forth(sys.argv[1] if len(sys.argv) > 1 else ": sq dup * ; 5 sq . 3 4 + ."))
