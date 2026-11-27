"""Manacher's algorithm: longest palindromic substring in O(n)."""


def longest_palindrome(s: str) -> str:
    t = "^#" + "#".join(s) + "#$"
    p = [0] * len(t)
    c = r = 0
    for i in range(1, len(t) - 1):
        if i < r:
            p[i] = min(r - i, p[2 * c - i])
        while t[i + p[i] + 1] == t[i - p[i] - 1]:
            p[i] += 1
        if i + p[i] > r:
            c, r = i, i + p[i]
    m = max(range(len(p)), key=p.__getitem__)
    start = (m - p[m]) // 2
    return s[start:start + p[m]]


if __name__ == "__main__":
    for w in ("babad", "forgeeksskeegfor", "a", ""):
        print(repr(w), "->", repr(longest_palindrome(w)))
