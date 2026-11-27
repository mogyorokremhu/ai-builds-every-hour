"""Fortune-cookie generator with lucky numbers. Usage: python fortune_cookie.py [count] [seed]"""
import random
import sys

OPENERS = ["A quiet moment", "An old friend", "The road ahead", "Your next idea", "Small patience", "A surprising door"]
VERBS = ["will bring", "is hiding", "carries", "soon reveals", "quietly protects", "is waiting to offer"]
GIFTS = ["unexpected luck", "a better question", "good soup", "a forgotten talent", "a well-timed laugh", "the answer you need"]
TAILS = ["before the week ends.", "if you look up from your phone.", "when you stop forcing it.", "closer than you think.", "on a rainy afternoon."]


def fortune(rng: random.Random) -> str:
    """Build one fortune with six lucky numbers."""
    text = f"{rng.choice(OPENERS)} {rng.choice(VERBS)} {rng.choice(GIFTS)} {rng.choice(TAILS)}"
    nums = sorted(rng.sample(range(1, 50), 6))
    return f"{text}\n  Lucky numbers: {' '.join(f'{n:02d}' for n in nums)}"


def main() -> None:
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    rng = random.Random(int(sys.argv[2])) if len(sys.argv) > 2 else random.Random()
    for _ in range(count):
        print(fortune(rng), end="\n\n")


if __name__ == "__main__":
    main()
