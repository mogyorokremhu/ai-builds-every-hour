"""Binary/hex conversion quiz. Usage: python binary_quiz.py [--auto] [--n 5] [--seed 1]"""
import argparse
import random


def make_question(rng: random.Random) -> tuple[str, int]:
    n = rng.randint(1, 255)
    if rng.random() < 0.5:
        return f"binary {n:b} in decimal", n
    return f"hex {n:X} in decimal", n


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--auto", action="store_true")
    p.add_argument("--n", type=int, default=5)
    p.add_argument("--seed", type=int, default=1)
    args = p.parse_args()
    rng = random.Random(args.seed)
    score = 0
    for i in range(1, args.n + 1):
        q, ans = make_question(rng)
        if args.auto:
            given = ans if rng.random() < 0.8 else ans ^ 1
            print(f"Q{i}: {q} = {given}")
        else:
            try:
                given = int(input(f"Q{i}: {q} = "))
            except (ValueError, EOFError):
                given = None
        if given == ans:
            score += 1
            print("  correct")
        else:
            print(f"  wrong, answer {ans}")
    print(f"Score: {score}/{args.n}")


if __name__ == "__main__":
    main()
