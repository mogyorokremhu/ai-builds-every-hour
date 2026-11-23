"""Generate absurd coffee-shop orders. Usage: python coffee_order.py [count] [seed]"""
import random
import sys

SIZES = ["tiny", "regular", "enormous", "bucket-sized"]
MILKS = ["oat", "almond", "whole", "no", "dragonfruit"]
BASES = ["espresso", "latte", "cold brew", "flat white", "mocha"]
EXTRAS = ["extra foam", "a cinnamon storm", "two sugars", "ice, but angry", "a tiny umbrella"]


def order(rng: random.Random) -> str:
    """Return one order string."""
    extras = rng.sample(EXTRAS, rng.randint(0, 2))
    tail = (" with " + " and ".join(extras)) if extras else ""
    return f"{rng.choice(SIZES)} {rng.choice(BASES)}, {rng.choice(MILKS)} milk{tail}"


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    rng = random.Random(int(sys.argv[2]) if len(sys.argv) > 2 else None)
    for i in range(1, n + 1):
        print(f"#{i}: {order(rng)}")
