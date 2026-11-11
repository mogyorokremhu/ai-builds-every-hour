"""Seeds (B2/S): every live cell dies each step; dead cells with exactly 2 neighbours are born."""
import sys


def step(live: set, w: int, h: int) -> set:
    counts: dict = {}
    for x, y in live:
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                if dx or dy:
                    p = ((x + dx) % w, (y + dy) % h)
                    counts[p] = counts.get(p, 0) + 1
    return {p for p, n in counts.items() if n == 2 and p not in live}


def render(live: set, w: int, h: int) -> str:
    return "\n".join("".join("#" if (x, y) in live else "." for x in range(w)) for y in range(h))


if __name__ == "__main__":
    gens = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    w, h = 30, 12
    live = {(14, 5), (15, 5)}
    for g in range(gens + 1):
        print(f"gen {g} ({len(live)} cells)")
        print(render(live, w, h))
        live = step(live, w, h)
