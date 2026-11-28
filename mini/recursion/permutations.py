"""Recursive permutations, subsets and combinations without itertools."""


def permutations(items: list) -> list[list]:
    """All orderings of items."""
    if len(items) <= 1:
        return [list(items)]
    out = []
    for i, x in enumerate(items):
        for p in permutations(items[:i] + items[i + 1:]):
            out.append([x] + p)
    return out


def subsets(items: list) -> list[list]:
    """The power set of items."""
    if not items:
        return [[]]
    rest = subsets(items[1:])
    return rest + [[items[0]] + s for s in rest]


def combinations(items: list, k: int) -> list[list]:
    """All k-element combinations, in input order."""
    if k == 0:
        return [[]]
    if len(items) < k:
        return []
    return [[items[0]] + c for c in combinations(items[1:], k - 1)] + combinations(items[1:], k)


if __name__ == "__main__":
    print(permutations([1, 2, 3]))
    print(subsets(["a", "b", "c"]))
    print(combinations([1, 2, 3, 4], 2))
    assert len(permutations(list(range(5)))) == 120
    assert len(subsets(list(range(6)))) == 64
