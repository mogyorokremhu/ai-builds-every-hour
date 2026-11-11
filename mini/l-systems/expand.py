"""Expand an L-system and print the string at each generation."""
import sys

SYSTEMS = {
    "algae": ("A", {"A": "AB", "B": "A"}),
    "koch": ("F", {"F": "F+F-F-F+F"}),
    "dragon": ("FX", {"X": "X+YF+", "Y": "-FX-Y"}),
    "plant": ("X", {"X": "F+[[X]-X]-F[-FX]+X", "F": "FF"}),
}


def expand(axiom: str, rules: dict[str, str], n: int) -> str:
    """Apply the rewrite rules n times."""
    s = axiom
    for _ in range(n):
        s = "".join(rules.get(c, c) for c in s)
    return s


def main() -> None:
    name = sys.argv[1] if len(sys.argv) > 1 else "algae"
    gens = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    axiom, rules = SYSTEMS[name]
    for g in range(gens + 1):
        s = expand(axiom, rules, g)
        print(f"{g}: {s if len(s) < 70 else s[:67] + '...'} (len {len(s)})")


if __name__ == "__main__":
    main()
