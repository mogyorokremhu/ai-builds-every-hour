"""Mini getopt-style argument parser: --long, --key=value, -abc flags, -o value, positionals."""


def parse_args(argv: list[str], takes_value: set[str] | None = None) -> tuple[dict, list[str]]:
    """Return (options, positionals). Names in `takes_value` consume the next argument."""
    takes_value = takes_value or set()
    opts: dict[str, object] = {}
    pos: list[str] = []
    i = 0
    while i < len(argv):
        a = argv[i]
        if a == "--":
            pos.extend(argv[i + 1:])
            break
        if a.startswith("--") and len(a) > 2:
            name, eq, val = a[2:].partition("=")
            if eq:
                opts[name] = val
            elif name in takes_value and i + 1 < len(argv):
                i += 1
                opts[name] = argv[i]
            else:
                opts[name] = True
        elif a.startswith("-") and len(a) > 1 and not a[1:].isdigit():
            for j, ch in enumerate(a[1:]):
                if ch in takes_value:
                    rest = a[2 + j:]
                    if rest:
                        opts[ch] = rest
                    elif i + 1 < len(argv):
                        i += 1
                        opts[ch] = argv[i]
                    break
                opts[ch] = True
        else:
            pos.append(a)
        i += 1
    return opts, pos


if __name__ == "__main__":
    o, p = parse_args(["-vx", "--name=bob", "-o", "out.txt", "file1", "--level", "3", "-5", "--", "-z"],
                      takes_value={"o", "level"})
    assert o == {"v": True, "x": True, "name": "bob", "o": "out.txt", "level": "3"}, o
    assert p == ["file1", "-5", "-z"], p
    print(o, p)
