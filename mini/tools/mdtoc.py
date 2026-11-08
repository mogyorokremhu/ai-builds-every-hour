"""Generate (or update in place) a table of contents for a Markdown file.

    python mdtoc.py README.md                 # print the TOC
    python mdtoc.py README.md --max 2         # only # and ## headings
    python mdtoc.py README.md --write         # insert/replace between <!-- toc --> markers
    python mdtoc.py --demo

Anchors follow GitHub's rules: lower-case, punctuation dropped, spaces to dashes, and
duplicates get ``-1``, ``-2`` suffixes. Headings inside fenced code blocks are ignored.
"""
from __future__ import annotations

import re
import sys
import unicodedata

START, END = "<!-- toc -->", "<!-- tocstop -->"
HEADING = re.compile(r"^(#{1,6})\s+(.+?)\s*#*\s*$")

DEMO = """# Emberdeep
Intro text.
<!-- toc -->
<!-- tocstop -->
## Getting started
### Install
### Run it!
## How to play
```python
# not a heading
```
### Items & loot
### Items & loot
## FAQ / troubleshooting
"""


def slug(text: str) -> str:
    text = re.sub(r"`([^`]*)`", r"\1", text)                  # inline code
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)      # links
    text = text.strip().lower()
    out = []
    for ch in text:
        cat = unicodedata.category(ch)
        if ch in " -":
            out.append("-" if ch == " " else ch)
        elif ch == "_" or cat[0] in "LN":
            out.append(ch)
    return "".join(out)


def headings(md: str, max_level: int = 6) -> list[tuple[int, str, str]]:
    """(level, title, anchor) for each heading, skipping code fences and the TOC itself."""
    out: list[tuple[int, str, str]] = []
    seen: dict[str, int] = {}
    fence = None
    for line in md.splitlines():
        stripped = line.lstrip()
        if stripped.startswith(("```", "~~~")):
            mark = stripped[:3]
            fence = None if fence == mark else (fence or mark)
            continue
        if fence:
            continue
        m = HEADING.match(line)
        if not m:
            continue
        level, title = len(m.group(1)), m.group(2)
        base = slug(title)
        n = seen.get(base, 0)
        seen[base] = n + 1
        anchor = base if n == 0 else f"{base}-{n}"
        if level <= max_level:
            out.append((level, title, anchor))
    return out


def toc(md: str, max_level: int = 6, skip_title: bool = True) -> list[str]:
    hs = headings(md, max_level)
    if skip_title and hs and hs[0][0] == 1 and sum(1 for h in hs if h[0] == 1) == 1:
        hs = hs[1:]
    if not hs:
        return []
    top = min(h[0] for h in hs)
    return [f"{'  ' * (lvl - top)}- [{title}](#{anchor})" for lvl, title, anchor in hs]


def write_toc(md: str, lines: list[str]) -> str:
    block = "\n".join([START, *lines, END])
    if START in md and END in md:
        a = md.index(START)
        b = md.index(END, a) + len(END)
        return md[:a] + block + md[b:]
    # after the first heading
    parts = md.split("\n", 1)
    return parts[0] + "\n\n" + block + "\n" + (parts[1] if len(parts) > 1 else "")


def main(argv: list[str]) -> int:
    args = list(argv)
    max_level = 6
    if "--max" in args:
        i = args.index("--max")
        max_level = int(args[i + 1])
        del args[i: i + 2]
    write = "--write" in args
    args = [a for a in args if a != "--write"]
    if not args or args[0] == "--demo":
        md, path = DEMO, None
    else:
        path = args[0]
        with open(path, encoding="utf-8") as fh:
            md = fh.read()
    lines = toc(md, max_level)
    if write and path:
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(write_toc(md, lines))
        print(f"updated {path} ({len(lines)} entries)")
    elif write:
        print(write_toc(md, lines))
    else:
        print("\n".join(lines) if lines else "(no headings)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
