"""Hangman: guess the word. Usage: python hangman.py [--auto]  (--auto plays itself)."""
import random
import sys

WORDS = ["python", "lisp", "bytecode", "dungeon", "hexagon", "compiler", "glider", "cipher"]
STAGES = ["", "O", "O|", "O|-", "-O|-", "-O|-/", "-O|-/\\"]


def play(word: str, guesses) -> bool:
    """Play one game with an iterator of guesses; return True on a win."""
    seen, misses = set(), 0
    for g in guesses:
        if g in seen:
            continue
        seen.add(g)
        if g not in word:
            misses += 1
        shown = " ".join(c if c in seen else "_" for c in word)
        print(f"{shown}   misses {misses}/6 {STAGES[misses]}")
        if all(c in seen for c in word):
            print("You win!")
            return True
        if misses >= 6:
            print(f"You lose. The word was {word}.")
            return False
    return False


def main() -> None:
    word = random.choice(WORDS)
    if "--auto" in sys.argv:
        order = "etaoinshrdlucmfwypvbgkjqxz"
        play(word, iter(order))
    else:
        def gen():
            while True:
                s = input("guess> ").strip().lower()
                if s:
                    yield s[0]
        try:
            play(word, gen())
        except EOFError:
            pass


if __name__ == "__main__":
    main()
