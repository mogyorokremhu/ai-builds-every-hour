"""Number lines of a file/stdin, optionally skipping blanks.
Usage: lineno.py [-b] [-w WIDTH] [file] | --selftest"""
import sys


def number(lines, skip_blank=False, width=4):
    n = 0
    for line in lines:
        line = line.rstrip("\n")
        if skip_blank and not line.strip():
            yield " " * width + "  " + line
            continue
        n += 1
        yield f"{n:>{width}}  {line}"


def selftest() -> None:
    assert list(number(["a\n", "b\n"], width=2)) == [" 1  a", " 2  b"]
    assert list(number(["a", "", "b"], skip_blank=True, width=1)) == ["1  a", "   ", "2  b"]
    print("lineno ok")


if __name__ == "__main__":
    a = sys.argv[1:]
    if a == ["--selftest"]:
        selftest()
        sys.exit()
    blank = "-b" in a
    w = 4
    if "-w" in a:
        w = int(a[a.index("-w") + 1])
    files = [x for i, x in enumerate(a) if not x.startswith("-") and not (i and a[i - 1] == "-w")]
    src = open(files[0]) if files else sys.stdin
    for out in number(src, blank, w):
        print(out)
