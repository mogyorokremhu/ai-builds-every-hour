"""True/false trivia with streak scoring. Usage: python trivia_streak.py [--auto] [--seed 1]"""
import argparse
import random

FACTS = [
    ("Honey never spoils.", True), ("Bananas grow on trees.", False),
    ("A day on Venus is longer than its year.", True), ("Humans have five senses only.", False),
    ("Octopuses have three hearts.", True), ("Lightning never strikes twice.", False),
    ("Water boils at lower temperature at altitude.", True), ("The Great Wall is visible from the Moon.", False),
]


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--auto", action="store_true")
    p.add_argument("--seed", type=int, default=1)
    args = p.parse_args()
    rng = random.Random(args.seed)
    facts = FACTS[:]
    rng.shuffle(facts)
    score = streak = best = 0
    for text, truth in facts:
        print(text)
        if args.auto:
            ans = truth if rng.random() < 0.8 else not truth
            print(f"> {'t' if ans else 'f'}")
        else:
            try:
                ans = input("t/f> ").strip().lower().startswith("t")
            except EOFError:
                ans = None
        if ans == truth:
            streak += 1
            best = max(best, streak)
            score += streak
            print(f"  right! streak {streak}")
        else:
            streak = 0
            print(f"  wrong, it is {truth}")
    print(f"Points: {score}  Best streak: {best}")


if __name__ == "__main__":
    main()
