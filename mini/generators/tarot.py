"""Random three-card spread (past / present / future) with whimsical meanings.

Usage: python tarot.py [seed]
"""
import random
import sys

CARDS = {
    "The Fool": "a leap into the unknown",
    "The Magician": "tools already in your hands",
    "The Tower": "sudden change that clears the ground",
    "The Star": "quiet hope returning",
    "The Moon": "things are not quite what they seem",
    "The Sun": "plain, warm success",
    "Strength": "patience beats force",
    "The Hermit": "a need for solitude and a lantern",
    "Wheel of Fortune": "luck turning over",
    "Justice": "consequences arriving on time",
    "Temperance": "mix, don't choose",
    "The Chariot": "momentum, if you hold the reins",
}


def spread(rng: random.Random) -> list[tuple[str, str, str, bool]]:
    """Return (position, card, meaning, reversed) for three distinct cards."""
    picks = rng.sample(sorted(CARDS), 3)
    return [(pos, c, CARDS[c], rng.random() < 0.3)
            for pos, c in zip(("Past", "Present", "Future"), picks)]


def main() -> None:
    rng = random.Random(int(sys.argv[1]) if len(sys.argv) > 1 else None)
    for pos, card, meaning, rev in spread(rng):
        tag = " (reversed)" if rev else ""
        print(f"{pos:8} {card}{tag}: {'the opposite of ' if rev else ''}{meaning}")


if __name__ == "__main__":
    main()
