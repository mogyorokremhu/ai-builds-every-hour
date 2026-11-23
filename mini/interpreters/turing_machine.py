"""Tiny Turing machine simulator; default program increments a binary number."""
from collections import defaultdict

# (state, symbol) -> (new_state, write, move)
INCREMENT = {
    ("right", "0"): ("right", "0", 1), ("right", "1"): ("right", "1", 1),
    ("right", "_"): ("carry", "_", -1),
    ("carry", "1"): ("carry", "0", -1), ("carry", "0"): ("halt", "1", 0),
    ("carry", "_"): ("halt", "1", 0),
}


def run(rules: dict, tape: str, state: str = "right", max_steps: int = 10_000) -> str:
    """Run the machine until 'halt' and return the tape contents."""
    cells = defaultdict(lambda: "_", enumerate(tape))
    pos = 0
    for _ in range(max_steps):
        if state == "halt":
            break
        state, cells[pos], move = rules[(state, cells[pos])]
        pos += move
    lo, hi = min(cells), max(cells)
    return "".join(cells[i] for i in range(lo, hi + 1)).strip("_")


if __name__ == "__main__":
    for n in ("0", "1011", "111"):
        print(n, "->", run(INCREMENT, n))
