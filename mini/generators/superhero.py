"""Superhero generator: name, power, weakness. Usage: python superhero.py [count] [seed]"""
import random
import sys

PREFIX = ["Captain", "Doctor", "Mister", "Lady", "Night", "Iron", "Storm", "Shadow", "Turbo"]
SUFFIX = ["Hawk", "Comet", "Badger", "Phantom", "Tide", "Lantern", "Moth", "Fist", "Sparrow"]
POWER = ["controls the weather", "talks to pigeons", "bends light", "never loses socks",
         "runs at the speed of Wi-Fi", "turns invisible when ignored", "can pause time for 3 seconds"]
WEAK = ["loud noises", "cold pizza", "Mondays", "tiny staircases", "unskippable ads", "wet sand"]


def hero(rng: random.Random) -> str:
    name = f"{rng.choice(PREFIX)} {rng.choice(SUFFIX)}"
    return f"{name}: {rng.choice(POWER)}; weakness: {rng.choice(WEAK)}"


if __name__ == "__main__":
    a = sys.argv[1:]
    rng = random.Random(int(a[1])) if len(a) > 1 else random.Random()
    for _ in range(int(a[0]) if a else 5):
        print(hero(rng))
