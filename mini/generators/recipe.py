"""Absurd recipe generator. Usage: python recipe.py [count] [seed]"""
import random
import sys

BASES = ["lentil", "pumpkin", "quinoa", "mushroom", "chickpea", "eggplant", "barley", "beet"]
STYLES = ["stew", "pie", "fritters", "risotto", "tacos", "curry", "casserole", "soup"]
SPICES = ["smoked paprika", "cumin", "star anise", "sumac", "cardamom", "fennel seed", "za'atar"]
EXTRAS = ["lemon zest", "toasted walnuts", "pickled onions", "tahini", "fresh dill", "chili oil", "feta"]
STEPS = ["Sweat the onions until translucent.", "Toast the {spice} in a dry pan for 30 seconds.",
         "Add the {base} and stir for {n} minutes.", "Simmer gently, covered, for {m} minutes.",
         "Finish with {extra} and a pinch of salt.", "Rest for {n} minutes before serving."]


def recipe(rng: random.Random) -> str:
    base, style = rng.choice(BASES), rng.choice(STYLES)
    spice, extra = rng.choice(SPICES), rng.choice(EXTRAS)
    lines = [f"== {spice.title()} {base.title()} {style.title()} =="]
    lines.append(f"Serves {rng.randint(2, 6)}. Ingredients: {base}, onion, {spice}, {extra}.")
    for i, s in enumerate(STEPS, 1):
        lines.append(f"{i}. " + s.format(spice=spice, base=base, extra=extra,
                                         n=rng.randint(2, 10), m=rng.randint(15, 45)))
    return "\n".join(lines)


if __name__ == "__main__":
    a = sys.argv[1:]
    rng = random.Random(int(a[1])) if len(a) > 1 else random.Random()
    for _ in range(int(a[0]) if a else 1):
        print(recipe(rng), end="\n\n")
