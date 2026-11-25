"""Pascal's triangle modulo m: rows, Sierpinski-style rendering, and Lucas' theorem check."""


def rows(n: int, m: int = 2) -> list[list[int]]:
    """First n rows of Pascal's triangle with entries reduced mod m."""
    out = [[1 % m]]
    for _ in range(n - 1):
        prev = out[-1]
        out.append([1 % m] + [(a + b) % m for a, b in zip(prev, prev[1:])] + [1 % m])
    return out


def lucas_binom_mod2(n: int, k: int) -> int:
    """C(n, k) mod 2 via Lucas: 1 iff k's bits are a subset of n's bits."""
    return 1 if (k & n) == k else 0


def render(n: int) -> str:
    """ASCII Sierpinski triangle from Pascal mod 2."""
    lines = []
    for i, r in enumerate(rows(n)):
        lines.append(" " * (n - i - 1) + " ".join("#" if x else "." for x in r))
    return "\n".join(lines)


if __name__ == "__main__":
    tri = rows(32)
    assert all(tri[i][j] == lucas_binom_mod2(i, j) for i in range(32) for j in range(i + 1))
    assert rows(5, 10)[4] == [1, 4, 6, 4, 1]
    print(render(16))
