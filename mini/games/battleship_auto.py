"""Battleship 8x8: hunt/target AI sinks a random fleet. `python battleship_auto.py [seed]` prints shots needed."""
import random
import sys

N = 8
SHIPS = (4, 3, 3, 2)


def place(rng):
    occ, ships = set(), []
    for L in SHIPS:
        while True:
            h = rng.random() < 0.5
            r, c = rng.randrange(N - (0 if h else L - 1)), rng.randrange(N - (L - 1 if h else 0))
            cells = {(r, c + i) if h else (r + i, c) for i in range(L)}
            if not cells & occ:
                occ |= cells
                ships.append(cells)
                break
    return ships


def play(rng):
    ships = place(rng)
    hits, shots, queue = set(), set(), []
    order = [(r, c) for r in range(N) for c in range(N) if (r + c) % 2 == 0]
    rng.shuffle(order)
    while any(not s <= hits for s in ships):
        if queue:
            t = queue.pop()
        else:
            t = next(p for p in order if p not in shots) if any(p not in shots for p in order) \
                else next((r, c) for r in range(N) for c in range(N) if (r, c) not in shots)
        if t in shots:
            continue
        shots.add(t)
        if any(t in s for s in ships):
            hits.add(t)
            r, c = t
            queue += [p for p in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1))
                      if 0 <= p[0] < N and 0 <= p[1] < N and p not in shots]
    return len(shots), shots, ships


def main():
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    n, shots, ships = play(random.Random(seed))
    allc = set().union(*ships)
    for r in range(N):
        print(" ".join("X" if (r, c) in shots and (r, c) in allc else "o" if (r, c) in shots else "." for c in range(N)))
    print(f"fleet sunk in {n} shots (of {N * N} cells)")
    avg = sum(play(random.Random(s))[0] for s in range(200)) / 200
    print(f"average over 200 games: {avg:.1f}")


if __name__ == "__main__":
    main()
