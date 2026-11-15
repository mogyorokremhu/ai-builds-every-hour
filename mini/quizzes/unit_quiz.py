"""Unit conversion quiz (answers within 1%). Usage: python unit_quiz.py [--auto] [--n 5] [--seed 1]"""
import argparse
import random

CONVERSIONS = [("km", "miles", 0.621371), ("kg", "pounds", 2.20462), ("liters", "gallons", 0.264172),
               ("meters", "feet", 3.28084), ("inches", "cm", 2.54)]


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--auto", action="store_true")
    p.add_argument("--n", type=int, default=5)
    p.add_argument("--seed", type=int, default=1)
    args = p.parse_args()
    rng = random.Random(args.seed)
    score = 0
    for i in range(1, args.n + 1):
        a, b, k = rng.choice(CONVERSIONS)
        x = rng.randint(2, 100)
        ans = x * k
        if args.auto:
            given = ans if rng.random() < 0.8 else ans * 1.5
            print(f"Q{i}: {x} {a} in {b} = {given:.2f}")
        else:
            try:
                given = float(input(f"Q{i}: {x} {a} in {b} = "))
            except (ValueError, EOFError):
                given = None
        if given is not None and abs(given - ans) <= 0.01 * ans:
            score += 1
            print("  correct")
        else:
            print(f"  wrong, answer {ans:.2f}")
    print(f"Score: {score}/{args.n}")


if __name__ == "__main__":
    main()
