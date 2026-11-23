"""Fredkin replicator (B1357/S02468): a cell lives if its neighbour count (Moore) is odd; patterns self-replicate."""
import sys


def step(live: set, w: int, h: int) -> set:
    counts: dict = {}
    for x, y in live:
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                if dx or dy:
                    p = ((x + dx) % w, (y + dy) % h)
                    counts[p] = counts.get(p, 0) + 1
    return {p for p, n in counts.items() if (p in live and n % 2 == 0 and n) or (p not in live and n % 2 == 1)}


def render(live: set, w: int, h: int) -> str:
    return "\n".join("".join("#" if (x, y) in live else "." for x in range(w)) for y in range(h))


if __name__ == "__main__":
    gens = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    w, h = 31, 15
    live = {(15, 7), (16, 7), (15, 8)}
    for g in range(gens + 1):
        print(f"gen {g} ({len(live)} cells)")
        print(render(live, w, h))
        live = step(live, w, h)
