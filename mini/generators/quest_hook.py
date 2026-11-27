"""RPG quest-hook generator. Usage: python quest_hook.py [count] [seed]"""
import random
import sys

GIVERS = ["A nervous innkeeper", "A retired knight", "A hooded stranger", "The village mayor", "A talking raven"]
TASKS = ["retrieve", "destroy", "escort", "decipher", "steal back"]
OBJECTS = ["a cursed lantern", "the baker's stolen recipe", "a map written in riddles", "a sleeping dragon's egg", "the lost crown"]
PLACES = ["the Whispering Marsh", "an abandoned mine", "the Clock Tower", "the frozen pass", "a sunken chapel"]
TWISTS = ["but someone you trust is lying.", "but time is running out.", "and the reward is not what it seems.", "but you are being followed."]


def hook(rng: random.Random) -> str:
    """One quest hook sentence."""
    return (f"{rng.choice(GIVERS)} asks you to {rng.choice(TASKS)} {rng.choice(OBJECTS)} "
            f"in {rng.choice(PLACES)}, {rng.choice(TWISTS)}")


def main() -> None:
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    rng = random.Random(int(sys.argv[2])) if len(sys.argv) > 2 else random.Random()
    for i in range(1, count + 1):
        print(f"{i}. {hook(rng)}")


if __name__ == "__main__":
    main()
