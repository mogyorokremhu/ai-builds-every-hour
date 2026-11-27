"""Knuth-Morris-Pratt substring search with failure table."""


def failure(p: str) -> list[int]:
    """Longest proper prefix that is also a suffix, per position."""
    f = [0] * len(p)
    k = 0
    for i in range(1, len(p)):
        while k and p[i] != p[k]:
            k = f[k - 1]
        if p[i] == p[k]:
            k += 1
        f[i] = k
    return f


def search(text: str, p: str) -> list[int]:
    """All start indices of p in text."""
    if not p:
        return []
    f, k, out = failure(p), 0, []
    for i, c in enumerate(text):
        while k and c != p[k]:
            k = f[k - 1]
        if c == p[k]:
            k += 1
        if k == len(p):
            out.append(i - k + 1)
            k = f[k - 1]
    return out


if __name__ == "__main__":
    print(failure("abacabab"))
    print(search("abababcabab", "abab"))
