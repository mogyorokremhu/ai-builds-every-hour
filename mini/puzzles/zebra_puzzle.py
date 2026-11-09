"""Einstein's zebra puzzle solved by permutation search with early pruning.

Usage: python zebra_puzzle.py
"""
from itertools import permutations


def solve():
    """Return the list of five houses (dicts) satisfying all 15 clues."""
    R = range(5)
    for col in permutations(R):  # col[c] = house position of that colour
        red, green, ivory, yellow, blue = col
        if green != ivory + 1:
            continue
        for nat in permutations(R):
            eng, spa, ukr, nor, jap = nat
            if eng != red or nor != 0 or abs(nor - blue) != 1:
                continue
            for drink in permutations(R):
                coffee, tea, milk, juice, water = drink
                if coffee != green or ukr != tea or milk != 2:
                    continue
                for smoke in permutations(R):
                    old, kools, chest, lucky, parl = smoke
                    if kools != yellow or lucky != juice or parl != jap:
                        continue
                    for pet in permutations(R):
                        dog, snail, fox, horse, zebra = pet
                        if spa != dog or old != snail:
                            continue
                        if abs(chest - fox) != 1 or abs(kools - horse) != 1:
                            continue
                        names = {
                            "color": ["red", "green", "ivory", "yellow", "blue"],
                            "nation": ["English", "Spaniard", "Ukrainian", "Norwegian", "Japanese"],
                            "drink": ["coffee", "tea", "milk", "juice", "water"],
                            "smoke": ["Old Gold", "Kools", "Chesterfield", "Lucky Strike", "Parliament"],
                            "pet": ["dog", "snail", "fox", "horse", "zebra"],
                        }
                        houses = [{} for _ in R]
                        for key, perm in (("color", col), ("nation", nat), ("drink", drink),
                                          ("smoke", smoke), ("pet", pet)):
                            for i, pos in enumerate(perm):
                                houses[pos][key] = names[key][i]
                        return houses
    return []


if __name__ == "__main__":
    hs = solve()
    for i, h in enumerate(hs, 1):
        print(i, h["color"].ljust(7), h["nation"].ljust(10), h["drink"].ljust(7),
              h["smoke"].ljust(13), h["pet"])
    z = next(h for h in hs if h["pet"] == "zebra")
    w = next(h for h in hs if h["drink"] == "water")
    print(f"The {z['nation']} owns the zebra; the {w['nation']} drinks water.")
