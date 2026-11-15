"""Word ladder: change one letter at a time. Plays itself by BFS: `python word_ladder.py [start end]`."""
import sys
from collections import deque

WORDS = """cold cord card ward warm worm word wood good gold bold bolt boat coat cost cast
cash cart care core cure pure pore pole pale male mile mine line fine fire hire hare
hard herd head heal heat meat melt malt mall tall tell tall ball bell belt best bust
dust duct deck dock lock look book boot boat moat mat cat cot dot dog log lot hot hat
rat bat bit sit sat set pet pen ten tan can cap cup pup pop top tip tap map mop""".split()


def neighbors(w, words):
    return [x for x in words if len(x) == len(w) and sum(a != b for a, b in zip(w, x)) == 1]


def ladder(start, end, words=WORDS):
    words = set(words) | {start, end}
    prev = {start: None}
    q = deque([start])
    while q:
        w = q.popleft()
        if w == end:
            path = []
            while w:
                path.append(w)
                w = prev[w]
            return path[::-1]
        for n in sorted(neighbors(w, words)):
            if n not in prev:
                prev[n] = w
                q.append(n)
    return None


def main():
    s, e = (sys.argv[1], sys.argv[2]) if len(sys.argv) > 2 else ("cold", "warm")
    p = ladder(s, e)
    print(" -> ".join(p) if p else f"no ladder from {s} to {e}")
    if len(sys.argv) <= 2:
        for a, b in (("cat", "dog"), ("head", "tail"), ("bat", "map")):
            p = ladder(a, b)
            print(" -> ".join(p) if p else f"no ladder from {a} to {b}")


if __name__ == "__main__":
    main()
