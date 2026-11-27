"""Subset construction: convert an NFA (no epsilons) to a DFA. Run: python nfa_to_dfa.py"""
from __future__ import annotations
from collections import deque


def subset_construction(alphabet, start, accepting, delta):
    """delta maps (state, symbol) -> set of states. Returns (dfa_start, dfa_accepting, dfa_delta)."""
    s0 = frozenset([start])
    table, seen, queue = {}, {s0}, deque([s0])
    while queue:
        cur = queue.popleft()
        for a in alphabet:
            nxt = frozenset(t for q in cur for t in delta.get((q, a), ()))
            table[(cur, a)] = nxt
            if nxt not in seen:
                seen.add(nxt)
                queue.append(nxt)
    acc = {s for s in seen if s & set(accepting)}
    return s0, acc, table


def run(word, start, acc, table):
    s = start
    for ch in word:
        s = table[(s, ch)]
    return s in acc


if __name__ == "__main__":
    # NFA for strings over {0,1} whose 3rd symbol from the end is 1
    delta = {("q0", "0"): {"q0"}, ("q0", "1"): {"q0", "q1"},
             ("q1", "0"): {"q2"}, ("q1", "1"): {"q2"},
             ("q2", "0"): {"q3"}, ("q2", "1"): {"q3"}}
    s, acc, table = subset_construction("01", "q0", {"q3"}, delta)
    print("DFA states:", len({k[0] for k in table}))
    for w in ["100", "0100", "011", "1110", "000"]:
        print(w, run(w, s, acc, table))
