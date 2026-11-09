"""Interactive REPL: `python repl.py` or `python repl.py file.lisp`."""
import sys
from lispling import global_env, run
from lispling.diagnostics import parse_checked
from lispling.types import LispError, to_string


def main() -> None:
    env = global_env()
    if len(sys.argv) > 1:
        run(open(sys.argv[1]).read(), env)
        return
    buf = ""
    while True:
        try:
            buf += input("lispling> " if not buf else "      ... ") + "\n"
        except EOFError:
            print()
            return
        if buf.count("(") > buf.count(")"):
            continue
        try:
            parse_checked(buf)  # precise line:col syntax errors
            r = run(buf, env)
            if r != []:
                print(to_string(r))
        except LispError as e:
            print("error:", e)
        buf = ""


if __name__ == "__main__":
    main()
