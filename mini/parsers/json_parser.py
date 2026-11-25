"""A tiny recursive-descent JSON parser (no json module), checked against it."""
import json


class Parser:
    def __init__(self, s: str):
        self.s, self.i = s, 0

    def ws(self):
        while self.i < len(self.s) and self.s[self.i] in " \t\r\n":
            self.i += 1

    def value(self):
        self.ws()
        c = self.s[self.i]
        if c == "{":
            return self.obj()
        if c == "[":
            return self.arr()
        if c == '"':
            return self.string()
        for lit, v in (("true", True), ("false", False), ("null", None)):
            if self.s.startswith(lit, self.i):
                self.i += len(lit)
                return v
        return self.number()

    def number(self):
        j = self.i
        while j < len(self.s) and self.s[j] in "+-0123456789.eE":
            j += 1
        if j == self.i:
            raise ValueError(f"unexpected {self.s[self.i]!r} at {self.i}")
        txt, self.i = self.s[self.i:j], j
        return float(txt) if any(ch in txt for ch in ".eE") else int(txt)

    def string(self):
        self.i += 1
        out = []
        while self.s[self.i] != '"':
            if self.s[self.i] == "\\":
                self.i += 1
                esc = self.s[self.i]
                if esc == "u":
                    out.append(chr(int(self.s[self.i + 1:self.i + 5], 16)))
                    self.i += 4
                else:
                    out.append({"n": "\n", "t": "\t", "r": "\r", "b": "\b", "f": "\f"}.get(esc, esc))
            else:
                out.append(self.s[self.i])
            self.i += 1
        self.i += 1
        return "".join(out)

    def arr(self):
        self.i += 1
        res = []
        self.ws()
        if self.s[self.i] == "]":
            self.i += 1
            return res
        while True:
            res.append(self.value())
            self.ws()
            c = self.s[self.i]
            self.i += 1
            if c == "]":
                return res
            if c != ",":
                raise ValueError(f"expected , or ] at {self.i - 1}")

    def obj(self):
        self.i += 1
        res = {}
        self.ws()
        if self.s[self.i] == "}":
            self.i += 1
            return res
        while True:
            self.ws()
            k = self.string()
            self.ws()
            if self.s[self.i] != ":":
                raise ValueError(f"expected : at {self.i}")
            self.i += 1
            res[k] = self.value()
            self.ws()
            c = self.s[self.i]
            self.i += 1
            if c == "}":
                return res
            if c != ",":
                raise ValueError(f"expected , or }} at {self.i - 1}")


def parse(s: str):
    return Parser(s).value()


if __name__ == "__main__":
    doc = '{"a": [1, 2.5, -3e2, true, null], "b": {"c": "x\\ny\\u0041"}, "d": []}'
    print(parse(doc))
    assert parse(doc) == json.loads(doc)
    print("matches json.loads")
