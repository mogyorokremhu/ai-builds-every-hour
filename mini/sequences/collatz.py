"""Collatz sequences: stopping times and the longest chain below a limit."""


def collatz(n: int) -> list[int]:
    """Return the Collatz chain from n down to 1."""
    chain = [n]
    while n != 1:
        n = n // 2 if n % 2 == 0 else 3 * n + 1
        chain.append(n)
    return chain


def longest_below(limit: int) -> tuple[int, int]:
    """Return (start, steps) with the longest chain for start < limit."""
    cache = {1: 0}

    def steps(n: int) -> int:
        path = []
        while n not in cache:
            path.append(n)
            n = n // 2 if n % 2 == 0 else 3 * n + 1
        base = cache[n]
        for i, m in enumerate(reversed(path), 1):
            cache[m] = base + i
        return cache[path[0]] if path else base

    best = (1, 0)
    for s in range(1, limit):
        c = steps(s)
        if c > best[1]:
            best = (s, c)
    return best


if __name__ == "__main__":
    assert collatz(6) == [6, 3, 10, 5, 16, 8, 4, 2, 1]
    assert longest_below(10) == (9, 19)
    print(collatz(27)[:10], "... len", len(collatz(27)))
    print("longest below 10000:", longest_below(10000))
