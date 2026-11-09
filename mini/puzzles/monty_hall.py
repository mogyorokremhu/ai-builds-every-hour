"""Monty Hall simulation: stay vs switch win rates.  Usage: monty_hall.py [games] [doors]"""
import random, sys

def play(doors, switch, rng):
    car, pick = rng.randrange(doors), rng.randrange(doors)
    opened = [d for d in range(doors) if d not in (car, pick)]
    host = rng.choice(opened)  # host opens one goat door
    if switch:
        pick = rng.choice([d for d in range(doors) if d not in (pick, host)])
    return pick == car

if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 100000
    d = int(sys.argv[2]) if len(sys.argv) > 2 else 3
    rng = random.Random(1)
    for name, sw in (("stay", False), ("switch", True)):
        w = sum(play(d, sw, rng) for _ in range(n))
        print(f"{name:6s} {w / n:.3f}")
