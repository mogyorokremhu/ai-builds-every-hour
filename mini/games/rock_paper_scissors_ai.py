"""Rock-paper-scissors vs an order-2 Markov predictor. `--auto` plays 300 rounds against a biased bot."""
import random
import sys
from collections import defaultdict

MOVES = "RPS"
BEATS = {"R": "P", "P": "S", "S": "R"}  # key is beaten by value


class Predictor:
    def __init__(self):
        self.table = defaultdict(lambda: defaultdict(int))
        self.hist = ""

    def predict(self) -> str:
        counts = self.table[self.hist[-2:]]
        if not counts:
            return random.choice(MOVES)
        return BEATS[max(counts, key=counts.get)]

    def update(self, move: str):
        self.table[self.hist[-2:]][move] += 1
        self.hist += move


def biased_bot(prev: str) -> str:
    return BEATS[prev] if prev and random.random() < 0.6 else random.choice(MOVES)


def result(ai: str, you: str) -> int:
    return 0 if ai == you else (1 if BEATS[you] == ai else -1)


def main():
    ai, wins, rounds, prev = Predictor(), 0, 0, ""
    auto = "--auto" in sys.argv
    while True:
        if auto:
            if rounds == 300:
                break
            you = biased_bot(prev)
        else:
            try:
                you = input("R/P/S> ").strip().upper()
            except EOFError:
                break
            if you not in MOVES:
                break
        pick = ai.predict()
        wins += result(pick, you)
        rounds += 1
        ai.update(you)
        prev = you
        if not auto:
            print(f"AI played {pick}; AI score {wins:+d}")
    print(f"{rounds} rounds, AI net score {wins:+d}")


if __name__ == "__main__":
    main()
