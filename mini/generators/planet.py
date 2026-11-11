"""Invent a random planet: name, climate, gravity, moons and a feature.

Usage: python planet.py [count] [seed]
"""
import random
import sys

START = ["Zor", "Kel", "Ny", "Tha", "Vor", "Mi", "Qua", "Ost"]
END = ["thos", "ria", "dune", "mir", "lax", "ion", "pera", "tek"]
CLIMATE = ["frozen", "scorching", "temperate", "storm-wracked", "swampy", "arid"]
FEATURE = ["ring of glass shards", "singing canyons", "floating forests",
           "tidal lava seas", "ruins of an older civilisation", "perpetual aurora"]


def planet(rng: random.Random) -> dict:
    """Return a dict describing one random planet."""
    return {
        "name": rng.choice(START) + rng.choice(END),
        "climate": rng.choice(CLIMATE),
        "gravity": round(rng.uniform(0.3, 2.5), 2),
        "moons": rng.choice([0, 0, 1, 1, 2, 3, 5]),
        "feature": rng.choice(FEATURE),
    }


def main() -> None:
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    rng = random.Random(int(sys.argv[2]) if len(sys.argv) > 2 else None)
    for _ in range(count):
        p = planet(rng)
        print(f"{p['name']}: {p['climate']}, {p['gravity']}g, "
              f"{p['moons']} moon(s), {p['feature']}")


if __name__ == "__main__":
    main()
