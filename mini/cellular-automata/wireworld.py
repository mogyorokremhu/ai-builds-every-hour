"""WireWorld: electrons running along a wire, with a gap-free branch."""
import sys

CIRCUIT = [
    "..................",
    ".tH@@@@@@@@@@tH@@.",
    "..................",
]
# '.' empty, '@' conductor, 'H' electron head, 't' electron tail


def step(g: list) -> list:
    h, w = len(g), len(g[0])
    out = []
    for y in range(h):
        row = ""
        for x in range(w):
            c = g[y][x]
            if c == "H":
                row += "t"
            elif c == "t":
                row += "@"
            elif c == "@":
                n = sum(g[y + dy][x + dx] == "H"
                        for dy in (-1, 0, 1) for dx in (-1, 0, 1)
                        if (dx or dy) and 0 <= y + dy < h and 0 <= x + dx < w)
                row += "H" if n in (1, 2) else "@"
            else:
                row += c
        out.append(row)
    return out


if __name__ == "__main__":
    gens = int(sys.argv[1]) if len(sys.argv) > 1 else 8
    g = list(CIRCUIT)
    for i in range(gens):
        print(f"gen {i}\n" + "\n".join(g) + "\n")
        g = step(g)
