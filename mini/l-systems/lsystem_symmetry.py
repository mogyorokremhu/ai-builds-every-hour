"""Check whether an L-system string is a palindrome or mirror-symmetric (+ <-> -)."""
from expand import expand

SYSTEMS = {
    "koch": ("F", {"F": "F+F-F-F+F"}),
    "dragon": ("FX", {"X": "X+YF+", "Y": "-FX-Y"}),
    "algae": ("A", {"A": "AB", "B": "A"}),
}


def mirror(s: str) -> str:
    return s.translate(str.maketrans("+-", "-+"))


def is_palindrome(s: str) -> bool:
    return s == s[::-1]


def is_mirror_symmetric(s: str) -> bool:
    """Reversed string with turns swapped equals the original."""
    return mirror(s[::-1]) == s


if __name__ == "__main__":
    for name, (axiom, rules) in SYSTEMS.items():
        for g in range(1, 5):
            s = expand(axiom, rules, g)
            print(f"{name:7} gen {g}: len={len(s):5d} palindrome={is_palindrome(s)!s:5} mirror={is_mirror_symmetric(s)}")
