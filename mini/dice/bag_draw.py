"""Fair 'bag' randomizer (like Tetris 7-bag): every face appears once per round."""
import random
import sys


def bag_rolls(sides: int, count: int, rng: random.Random) -> list[int]:
    """Roll a die with `sides` faces using shuffled bags so streaks stay short."""
    out: list[int] = []
    while len(out) < count:
        bag = list(range(1, sides + 1))
        rng.shuffle(bag)
        out.extend(bag)
    return out[:count]


def main() -> None:
    sides = int(sys.argv[1]) if len(sys.argv) > 1 else 6
    count = int(sys.argv[2]) if len(sys.argv) > 2 else 24
    rolls = bag_rolls(sides, count, random.Random(7))
    print(" ".join(map(str, rolls)))
    print("max gap between repeats of a face is at most", 2 * sides - 1)


if __name__ == "__main__":
    main()
