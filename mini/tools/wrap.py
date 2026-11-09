"""Word-wrap stdin to a width: python wrap.py [-w 60] [-j]  (-j justifies)."""
import sys, textwrap


def justify(line, width):
    words = line.split()
    if len(words) < 2:
        return line
    gaps, spaces = len(words) - 1, width - sum(map(len, words))
    out = ""
    for i, w in enumerate(words[:-1]):
        out += w + " " * (spaces // gaps + (1 if i < spaces % gaps else 0))
    return out + words[-1]


def wrap(text, width=60, just=False):
    lines = textwrap.wrap(text, width)
    if just:
        lines = [justify(l, width) for l in lines[:-1]] + lines[-1:]
    return "\n".join(lines)


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        r = wrap("the quick brown fox jumps over the lazy dog", 15, True)
        assert all(len(l) == 15 for l in r.split("\n")[:-1]), r
        print("ok")
        sys.exit()
    a = sys.argv[1:]
    w = int(a[a.index("-w") + 1]) if "-w" in a else 60
    print(wrap(sys.stdin.read(), w, "-j" in a))
