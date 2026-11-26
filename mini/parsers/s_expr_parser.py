"""S-expression reader: parses '(a (b 1) "str" 2.5)' into nested Python lists, and prints back."""
import re

TOKEN = re.compile(r'\s*(?:(\()|(\))|"((?:[^"\\]|\\.)*)"|([^\s()"]+))')


def tokenize(src: str) -> list[tuple[str, str]]:
    out, pos = [], 0
    src = src.rstrip()
    while pos < len(src):
        m = TOKEN.match(src, pos)
        if not m:
            raise ValueError(f"bad input at {pos}")
        pos = m.end()
        if m.group(1):
            out.append(("(", "("))
        elif m.group(2):
            out.append((")", ")"))
        elif m.group(3) is not None:
            out.append(("str", m.group(3).replace('\\"', '"')))
        else:
            out.append(("atom", m.group(4)))
    return out


def parse(src: str):
    """Parse exactly one s-expression."""
    toks = tokenize(src)
    val, i = _read(toks, 0)
    if i != len(toks):
        raise ValueError("trailing tokens")
    return val


def _read(toks, i):
    if i >= len(toks):
        raise ValueError("unexpected end")
    kind, text = toks[i]
    if kind == "(":
        items, i = [], i + 1
        while i < len(toks) and toks[i][0] != ")":
            item, i = _read(toks, i)
            items.append(item)
        if i >= len(toks):
            raise ValueError("missing )")
        return items, i + 1
    if kind == ")":
        raise ValueError("unexpected )")
    if kind == "str":
        return text, i + 1
    for typ in (int, float):
        try:
            return typ(text), i + 1
        except ValueError:
            pass
    return ("sym", text), i + 1


def show(v) -> str:
    if isinstance(v, list):
        return "(" + " ".join(show(x) for x in v) + ")"
    if isinstance(v, tuple):
        return v[1]
    if isinstance(v, str):
        return '"' + v.replace('"', '\\"') + '"'
    return str(v)


if __name__ == "__main__":
    src = '(define (f x) (+ x 1.5 "a b"))'
    tree = parse(src)
    assert show(tree) == src, show(tree)
    assert parse("(1 (2 3))") == [1, [2, 3]]
    print(tree)
