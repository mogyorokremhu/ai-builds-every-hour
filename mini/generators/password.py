"""Memorable passphrase generator: word-word-number style.

Usage: python password.py [count] [words] [seed]
"""
import random
import sys

WORDS = ("amber basil cedar dune ember fjord glade harbor iris juniper kelp lantern "
         "meadow nectar orchid pebble quartz river saffron thistle umber velvet willow "
         "yarrow zephyr maple coral falcon granite hollow ivory lotus mist onyx").split()


def passphrase(rng: random.Random, words: int = 3) -> str:
    """Return a hyphenated passphrase ending in a two-digit number."""
    parts = [rng.choice(WORDS) for _ in range(words)]
    return "-".join(w.capitalize() if i % 2 == 0 else w for i, w in enumerate(parts)) + f"-{rng.randrange(10, 100)}"


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    w = int(sys.argv[2]) if len(sys.argv) > 2 else 3
    rng = random.Random(int(sys.argv[3])) if len(sys.argv) > 3 else random.Random()
    for _ in range(n):
        print(passphrase(rng, w))
