"""Multiple-choice capitals quiz. Usage: python capitals_quiz.py [--auto] [--n 5] [--seed 1]"""
import argparse
import random

CAPITALS = {
    "France": "Paris", "Japan": "Tokyo", "Hungary": "Budapest", "Canada": "Ottawa",
    "Brazil": "Brasilia", "Egypt": "Cairo", "Australia": "Canberra", "Kenya": "Nairobi",
    "Norway": "Oslo", "Peru": "Lima", "Poland": "Warsaw", "Turkey": "Ankara",
}


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--auto", action="store_true")
    p.add_argument("--n", type=int, default=5)
    p.add_argument("--seed", type=int, default=1)
    args = p.parse_args()
    rng = random.Random(args.seed)
    score = 0
    for i, country in enumerate(rng.sample(list(CAPITALS), args.n), 1):
        right = CAPITALS[country]
        options = rng.sample([c for c in CAPITALS.values() if c != right], 3) + [right]
        rng.shuffle(options)
        print(f"Q{i}: Capital of {country}?")
        for k, o in enumerate(options):
            print(f"  {'ABCD'[k]}) {o}")
        if args.auto:
            pick = options.index(right) if rng.random() < 0.75 else rng.randrange(4)
            print(f"> {'ABCD'[pick]}")
        else:
            try:
                pick = "ABCD".index(input("> ").strip().upper()[:1])
            except (ValueError, EOFError):
                pick = -1
        if pick >= 0 and options[pick] == right:
            score += 1
    print(f"Score: {score}/{args.n}")


if __name__ == "__main__":
    main()
