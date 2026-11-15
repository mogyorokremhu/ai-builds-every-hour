"""Validate an L-system: unknown symbols, bracket balance, and growth per generation."""
import sys

SYSTEMS = {
    "plant": ("X", {"X": "F+[[X]-X]-F[-FX]+X", "F": "FF"}),
    "koch": ("F", {"F": "F+F-F-F+F"}),
    "broken": ("F", {"F": "F[+F[-F"}),
}
TURTLE = set("F+-[]X")


def check(axiom: str, rules: dict, gens: int = 4) -> list[str]:
    problems = []
    s = axiom
    for g in range(1, gens + 1):
        s = "".join(rules.get(c, c) for c in s)
        depth = 0
        for c in s:
            depth += (c == "[") - (c == "]")
            if depth < 0:
                break
        if depth != 0:
            problems.append(f"gen {g}: unbalanced brackets (depth {depth})")
            break
    odd = sorted({c for c in s if c not in TURTLE})
    if odd:
        problems.append(f"unknown turtle symbols: {''.join(odd)}")
    return problems


if __name__ == "__main__":
    names = sys.argv[1:] or list(SYSTEMS)
    for name in names:
        axiom, rules = SYSTEMS[name]
        issues = check(axiom, rules)
        print(f"{name}: {'OK' if not issues else '; '.join(issues)}")
