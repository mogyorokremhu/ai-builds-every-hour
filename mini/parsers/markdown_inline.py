"""Tiny recursive Markdown inline parser: **bold**, *italic*, `code`, [text](url)
-> HTML, with escaping."""
import html


def render(s: str) -> str:
    out, i = [], 0
    while i < len(s):
        c = s[i]
        if c == "\\" and i + 1 < len(s):
            out.append(html.escape(s[i + 1]))
            i += 2
        elif c == "`" and (j := s.find("`", i + 1)) > 0:
            out.append("<code>" + html.escape(s[i + 1:j]) + "</code>")
            i = j + 1
        elif s.startswith("**", i) and (j := s.find("**", i + 2)) > 0:
            while s.startswith("*", j + 2):
                j += 1
            out.append("<strong>" + render(s[i + 2:j]) + "</strong>")
            i = j + 2
        elif c == "*" and (j := s.find("*", i + 1)) > 0:
            out.append("<em>" + render(s[i + 1:j]) + "</em>")
            i = j + 1
        elif c == "[" and (j := s.find("](", i)) > 0 and (k := s.find(")", j)) > 0:
            out.append('<a href="%s">%s</a>' % (html.escape(s[j + 2:k], quote=True), render(s[i + 1:j])))
            i = k + 1
        else:
            out.append(html.escape(c))
            i += 1
    return "".join(out)


if __name__ == "__main__":
    cases = {
        "plain <b>": "plain &lt;b&gt;",
        "**bold *and italic***": "<strong>bold <em>and italic</em></strong>",
        "use `a<b` here": "use <code>a&lt;b</code> here",
        "[site](http://x.io?a=1&b=2)": '<a href="http://x.io?a=1&amp;b=2">site</a>',
        r"\*not italic\*": "*not italic*",
    }
    for src, want in cases.items():
        got = render(src)
        assert got == want, (src, got, want)
        print(f"{src!r} -> {got}")
    print("markdown_inline: all checks passed")
