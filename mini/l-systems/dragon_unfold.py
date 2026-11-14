"""Dragon curve by paper folding: the turn sequence without any rewriting.

Prints the turn string for N folds and checks it against the L-system version.
"""


def fold_turns(n: int) -> str:
    t = ""
    for _ in range(n):
        t = t + "R" + "".join("L" if c == "R" else "R" for c in reversed(t))
    return t


def lsystem_turns(n: int) -> str:
    s = "FX"
    for _ in range(n):
        s = "".join({"X": "X+YF", "Y": "FX-Y"}.get(c, c) for c in s)
    return "".join("R" if c == "+" else "L" for c in s if c in "+-")


if __name__ == "__main__":
    for n in range(1, 7):
        t = fold_turns(n)
        print(n, t if n < 5 else t[:32] + "...", len(t))
    print("matches L-system:", fold_turns(5) == lsystem_turns(5))
