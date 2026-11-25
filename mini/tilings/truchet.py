"""Truchet tiles in ASCII: each cell is randomly '/' or '\\', forming maze-like patterns."""
import random


def truchet(width: int = 40, height: int = 12, seed: int | None = 7) -> str:
    rng = random.Random(seed)
    return "\n".join("".join(rng.choice("/\\") for _ in range(width)) for _ in range(height))


if __name__ == "__main__":
    art = truchet()
    print(art)
    assert len(art.splitlines()) == 12 and set(art) <= set("/\\\n")
