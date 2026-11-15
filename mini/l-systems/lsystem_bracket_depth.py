"""Report maximum branching depth and branch count of an L-system string per generation."""
RULES = {"X": "F[+X][-X]FX", "F": "FF"}


def stats(s: str) -> tuple[int, int]:
    depth = best = branches = 0
    for c in s:
        if c == "[":
            depth += 1
            branches += 1
            best = max(best, depth)
        elif c == "]":
            depth -= 1
    return best, branches


if __name__ == "__main__":
    s = "X"
    print("gen  length  max-depth  branches")
    for g in range(0, 7):
        d, b = stats(s)
        print(f"{g:>3} {len(s):>7} {d:>10} {b:>9}")
        s = "".join(RULES.get(c, c) for c in s)
