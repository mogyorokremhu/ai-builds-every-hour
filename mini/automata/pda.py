"""Tiny pushdown automaton: balanced brackets and a^n b^n. Run: python pda.py"""


def balanced(word: str) -> bool:
    pairs = {")": "(", "]": "[", "}": "{"}
    stack = []
    for ch in word:
        if ch in "([{":
            stack.append(ch)
        elif ch in pairs:
            if not stack or stack.pop() != pairs[ch]:
                return False
    return not stack


def anbn(word: str) -> bool:
    stack, phase = [], "push"
    for ch in word:
        if ch == "a" and phase == "push":
            stack.append("A")
        elif ch == "b" and stack:
            phase = "pop"
            stack.pop()
        else:
            return False
    return not stack


if __name__ == "__main__":
    for w in ["([]{})", "([)]", "((", ""]:
        print(f"balanced({w!r}) = {balanced(w)}")
    for w in ["aabb", "aab", "abab", ""]:
        print(f"anbn({w!r}) = {anbn(w)}")
