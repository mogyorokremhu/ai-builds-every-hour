"""Generate arithmetic "think of a number" riddles with their answers.

Usage: python riddle_math.py [count] [seed]
"""
import random
import sys


def riddle(rng: random.Random) -> tuple[str, int]:
    """Build a riddle by applying random steps to a secret number."""
    n = rng.randint(2, 20)
    value, steps = n, []
    for _ in range(3):
        op = rng.choice("+-*")
        k = rng.randint(2, 9)
        if op == "+":
            value += k
            steps.append(f"add {k}")
        elif op == "-":
            value -= k
            steps.append(f"subtract {k}")
        else:
            value *= k
            steps.append(f"multiply by {k}")
    return f"I think of a number, {', then '.join(steps)}, and get {value}. What was it?", n


def main() -> None:
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    rng = random.Random(int(sys.argv[2]) if len(sys.argv) > 2 else None)
    for i in range(1, count + 1):
        text, answer = riddle(rng)
        print(f"{i}. {text}\n   Answer: {answer}")


if __name__ == "__main__":
    main()
