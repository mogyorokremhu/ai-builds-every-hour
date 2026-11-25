"""Which day of the week was a given date? Usage: python weekday_quiz.py [--auto] [--n 5] [--seed 1]"""
import argparse
import random


def make_question(rng: random.Random) -> tuple[str, str]:
    import datetime
    d = datetime.date(rng.randint(1990, 2030), rng.randint(1, 12), rng.randint(1, 28))
    return f"Weekday of {d.isoformat()} =", d.strftime("%A")


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
