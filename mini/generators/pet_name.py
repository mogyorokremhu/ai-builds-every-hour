"""Pet-name generator: cute, regal or silly names by species. Usage: python pet_name.py [count] [seed]"""
import random
import sys

PARTS = {
    "cat": (["Mister", "Lady", "Captain", "Professor"], ["Whiskers", "Biscuit", "Mochi", "Pickle", "Noodle"]),
    "dog": (["Sir", "Duke", "Doctor", "General"], ["Waffles", "Barkley", "Tater", "Bruno", "Sprout"]),
    "bird": (["Admiral", "Madame", "Baron", "Count"], ["Feathers", "Pip", "Tweedle", "Squawk", "Mango"]),
    "fish": (["Sergeant", "Queen", "King", "Lord"], ["Bubbles", "Fin", "Splash", "Nemo-ish", "Gill"]),
}


def pet(rng: random.Random) -> str:
    """Return 'species: Title Name'."""
    species = rng.choice(sorted(PARTS))
    titles, names = PARTS[species]
    return f"{species}: {rng.choice(titles)} {rng.choice(names)}"


def main() -> None:
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 8
    rng = random.Random(int(sys.argv[2])) if len(sys.argv) > 2 else random.Random()
    for _ in range(count):
        print(pet(rng))


if __name__ == "__main__":
    main()
