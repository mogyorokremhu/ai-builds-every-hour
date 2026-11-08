#!/usr/bin/env python3
"""Text case/slug converter: slug, snake, kebab, camel, pascal, title, constant — accents folded.

usage: slug.py [-s kebab] "Hello Wörld, it's 2026!"     slug.py --all "some text"     slug.py --selftest
"""
import re, sys, unicodedata

def words(text):
    text = unicodedata.normalize("NFKD", text)
    text = "".join(c for c in text if not unicodedata.combining(c))
    text = re.sub(r"([a-z0-9])([A-Z])", r"\1 \2", text)   # split camelCase
    text = text.replace("'", "")
    return [w.lower() for w in re.findall(r"[A-Za-z0-9]+", text)]

STYLES = {
    "slug": lambda w: "-".join(w),
    "kebab": lambda w: "-".join(w),
    "snake": lambda w: "_".join(w),
    "constant": lambda w: "_".join(w).upper(),
    "camel": lambda w: w[0] + "".join(x.capitalize() for x in w[1:]) if w else "",
    "pascal": lambda w: "".join(x.capitalize() for x in w),
    "title": lambda w: " ".join(x.capitalize() for x in w),
}

def convert(text, style="slug"):
    return STYLES[style](words(text))

def selftest():
    assert convert("Hello Wörld, it's 2026!") == "hello-world-its-2026"
    assert convert("parseHttpResponse", "snake") == "parse_http_response"
    assert convert("some_var-name here", "camel") == "someVarNameHere"
    assert convert("déjà vu", "pascal") == "DejaVu"
    assert convert("max retries", "constant") == "MAX_RETRIES"
    assert convert("", "camel") == ""
    print("slug: ok")

if __name__ == "__main__":
    args = sys.argv[1:]
    if "--selftest" in args:
        selftest()
    else:
        style = "slug"
        if "-s" in args:
            i = args.index("-s"); style = args[i + 1]; del args[i:i + 2]
        show_all = "--all" in args
        args = [a for a in args if a != "--all"]
        text = " ".join(args) or sys.stdin.read()
        if show_all:
            for s in ("slug", "snake", "camel", "pascal", "title", "constant"):
                print(f"{s:9}{convert(text, s)}")
        else:
            print(convert(text, style))
