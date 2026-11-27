"""DFA simulator with a few example machines. Run: python dfa.py"""
from __future__ import annotations


class DFA:
    def __init__(self, start, accepting, delta):
        self.start, self.accepting, self.delta = start, set(accepting), delta

    def accepts(self, word: str) -> bool:
        state = self.start
        for ch in word:
            state = self.delta.get((state, ch))
            if state is None:
                return False
        return state in self.accepting


def divisible_by(n: int) -> DFA:
    """Binary strings whose value is divisible by n."""
    delta = {(r, b): (r * 2 + int(b)) % n for r in range(n) for b in "01"}
    return DFA(0, {0}, delta)


def ends_with_ab() -> DFA:
    delta = {(0, "a"): 1, (0, "b"): 0, (1, "a"): 1, (1, "b"): 2,
             (2, "a"): 1, (2, "b"): 0}
    return DFA(0, {2}, delta)


if __name__ == "__main__":
    d3 = divisible_by(3)
    for w in ["0", "11", "110", "101", "1001"]:
        print(f"{w:>5} divisible by 3? {d3.accepts(w)}")
    e = ends_with_ab()
    for w in ["ab", "aab", "aba", "bab", ""]:
        print(f"{w!r:>6} ends with ab? {e.accepts(w)}")
