"""Word-level Markov text generator trained on a built-in sample (or a file arg).
Usage: python markov.py [file] [words] [seed]"""
import random
import sys
from collections import defaultdict

SAMPLE = """The robot built a tower every hour and the tower grew taller every hour.
Nobody watched the robot but the robot kept building because building was the point.
The tower leaned in the wind and the robot built a bridge to hold the tower.
Every bridge needs a river and every river needs a robot to count the stones."""


def train(text: str, order: int = 2):
    words = text.split()
    table = defaultdict(list)
    for i in range(len(words) - order):
        table[tuple(words[i:i + order])].append(words[i + order])
    return table


def generate(table, n: int, rng: random.Random, order: int = 2) -> str:
    key = rng.choice(list(table))
    out = list(key)
    while len(out) < n:
        nxt = table.get(tuple(out[-order:]))
        if not nxt:
            key = rng.choice(list(table))
            out.extend(key)
            continue
        out.append(rng.choice(nxt))
    return " ".join(out[:n])


if __name__ == "__main__":
    a = sys.argv[1:]
    text = open(a[0]).read() if a and not a[0].isdigit() else SAMPLE
    rest = [x for x in a if x.isdigit()]
    n = int(rest[0]) if rest else 40
    rng = random.Random(int(rest[1])) if len(rest) > 1 else random.Random()
    print(generate(train(text), n, rng))
