"""Template-based haiku generator (5-7-5 by pre-counted syllables).

Usage: python haiku.py [count] [seed]
"""
import random
import sys

FIVE = ["silent autumn rain", "the old pond awakes", "cold wind through the pines", "morning light unfolds"]
SEVEN = ["a single leaf drifts downstream", "shadows stretch across the hills", "the lantern flickers and fades", "mist rises from sleeping fields"]
FIVE2 = ["frogs begin to sing", "the moon grows heavy", "snow keeps its secrets", "petals touch the ground"]


def haiku(rng: random.Random) -> str:
    """Return a three-line haiku."""
    return "\n".join([rng.choice(FIVE), rng.choice(SEVEN), rng.choice(FIVE2)])


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    rng = random.Random(int(sys.argv[2])) if len(sys.argv) > 2 else random.Random()
    print("\n\n".join(haiku(rng) for _ in range(n)))
