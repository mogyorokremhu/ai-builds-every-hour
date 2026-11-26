"""Write and read plain-text PBM (P1) bitmaps; prints one to stdout as a demo."""


def to_pbm(rows: list[str]) -> str:
    """Convert '#'/'.' rows into a P1 PBM string."""
    w, h = len(rows[0]), len(rows)
    body = "\n".join(" ".join("1" if c == "#" else "0" for c in r) for r in rows)
    return f"P1\n{w} {h}\n{body}\n"


def from_pbm(text: str) -> list[str]:
    """Parse a P1 PBM back into '#'/'.' rows."""
    tokens = [t for line in text.splitlines() if not line.startswith("#") for t in line.split()]
    assert tokens[0] == "P1", "not a P1 PBM"
    w, h = int(tokens[1]), int(tokens[2])
    bits = tokens[3:]
    return ["".join("#" if bits[y * w + x] == "1" else "." for x in range(w)) for y in range(h)]


if __name__ == "__main__":
    art = ["#...#", ".#.#.", "..#..", ".#.#.", "#...#"]
    pbm = to_pbm(art)
    print(pbm)
    assert from_pbm(pbm) == art
    print("round trip ok")
