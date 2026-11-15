"""Roman numeral quiz. Usage: python roman_quiz.py [--auto] [--n 5] [--seed 1]"""
import argparse
import random

PAIRS = [(1000, "M"), (900, "CM"), (500, "D"), (400, "CD"), (100, "C"), (90, "XC"),
         (50, "L"), (40, "XL"), (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I")]


def to_roman(n: int) -> str:
    out = ""
    for v, s in PAIRS:
        while n >= v:
            out += s
            n -= v
    return out


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--auto", action="store_true")
    p.add_argument("--n", type=int, default=5)
    p.add_argument("--seed", type=int, default=1)
    args = p.parse_args()
    rng = random.Random(args.seed)
    score = 0
    for i in range(1, args.n + 1):
        n = rng.randint(1, 3999)
        ans = to_roman(n)
        if args.auto:
            given = ans if rng.random() < 0.8 else to_roman(n + 1)
            print(f"Q{i}: {n} in Roman = {given}")
        else:
            try:
                given = input(f"Q{i}: {n} in Roman = ").strip().upper()
            except EOFError:
                given = ""
        if given == ans:
            score += 1
            print("  correct")
        else:
            print(f"  wrong, answer {ans}")
    print(f"Score: {score}/{args.n}")


if __name__ == "__main__":
    main()
