"""Collatz records: for each limit, the start value with the longest chain (memoised)."""


def chain_lengths(limit: int) -> list[int]:
    """Return steps-to-1 for every n < limit using a memo table."""
    steps = [0] * limit
    for n in range(2, limit):
        x, count = n, 0
        while x >= n or x == 0:
            x = x // 2 if x % 2 == 0 else 3 * x + 1
            count += 1
            if x < n:
                break
        steps[n] = count + steps[x]
    return steps


def records(limit: int) -> list[tuple[int, int]]:
    """Starts that beat every smaller start's chain length."""
    steps = chain_lengths(limit)
    best, out = -1, []
    for n in range(1, limit):
        if steps[n] > best:
            best = steps[n]
            out.append((n, best))
    return out


if __name__ == "__main__":
    for n, s in records(100000):
        print(f"{n:>6} -> {s} steps")
    assert records(30)[-1] == (27, 111)
