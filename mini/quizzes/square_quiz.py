"""Squares and cubes quiz. Usage: python square_quiz.py [--auto] [--n 5] [--seed 1]"""
import argparse
import random


def make_question(rng: random.Random) -> tuple[str, str]:
    if rng.random() < 0.7:
        n = rng.randint(2, 25)
        return f"{n}^2 =", str(n * n)
    n = rng.randint(2, 10)
    return f"{n}^3 =", str(n ** 3)


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
            given = ans if rng.random() < 0.8 else "?"
            print(f"Q{i}: {q} {given}")
        else:
            try:
                given = input(f"Q{i}: {q} ").strip()
            except EOFError:
                given = ""
        if given.lower() == ans.lower():
            score += 1
        else:
            print(f"  wrong, answer: {ans}")
    print(f"Score: {score}/{args.n}")


if __name__ == "__main__":
    main()
