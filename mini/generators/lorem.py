"""Lorem-ipsum-style filler text generator.

Usage: python lorem.py [paragraphs] [seed]
"""
import random
import sys

WORDS = ("lorem ipsum dolor sit amet consectetur adipiscing elit sed do eiusmod tempor incididunt ut labore et "
         "dolore magna aliqua enim ad minim veniam quis nostrud exercitation ullamco laboris nisi aliquip ex ea "
         "commodo consequat duis aute irure in reprehenderit voluptate velit esse cillum fugiat nulla pariatur").split()


def sentence(rng: random.Random) -> str:
    """Return one sentence of 6-14 words, capitalised, with an optional comma."""
    words = [rng.choice(WORDS) for _ in range(rng.randint(6, 14))]
    if len(words) > 8 and rng.random() < 0.6:
        words[rng.randint(3, len(words) - 3)] += ","
    return " ".join(words).capitalize() + "."


def paragraph(rng: random.Random) -> str:
    """Return a paragraph of 3-6 sentences."""
    return " ".join(sentence(rng) for _ in range(rng.randint(3, 6)))


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    rng = random.Random(int(sys.argv[2])) if len(sys.argv) > 2 else random.Random()
    print("\n\n".join(paragraph(rng) for _ in range(n)))
