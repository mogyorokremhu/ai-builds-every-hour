"""Rock band name + album title generator. Usage: python band_name.py [count] [seed]"""
import random
import sys

ADJ = ["Electric", "Velvet", "Hollow", "Neon", "Feral", "Crimson", "Silent", "Rusty", "Cosmic"]
NOUN = ["Wolves", "Parade", "Engines", "Harbor", "Pigeons", "Lanterns", "Orchard", "Static", "Ghosts"]
ALBUM = ["Songs for {n}", "Tides of {n}", "The Last {n}", "{n} Forever", "Return to {n}"]


def band(rng: random.Random) -> str:
    form = rng.choice(("The {a} {n}", "{a} {n}", "{n} of {a2}"))
    return form.format(a=rng.choice(ADJ), n=rng.choice(NOUN), a2=rng.choice(ADJ))


if __name__ == "__main__":
    a = sys.argv[1:]
    rng = random.Random(int(a[1])) if len(a) > 1 else random.Random()
    for _ in range(int(a[0]) if a else 5):
        print(f"{band(rng)} — \"{rng.choice(ALBUM).format(n=rng.choice(NOUN))}\" ({rng.randint(1969, 2026)})")
