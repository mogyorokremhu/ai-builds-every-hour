"""Z-algorithm: z[i] = length of longest common prefix of s and s[i:]."""


def z_array(s: str) -> list[int]:
    n = len(s)
    z = [0] * n
    if n:
        z[0] = n
    l = r = 0
    for i in range(1, n):
        if i < r:
            z[i] = min(r - i, z[i - l])
        while i + z[i] < n and s[z[i]] == s[i + z[i]]:
            z[i] += 1
        if i + z[i] > r:
            l, r = i, i + z[i]
    return z


def find(text: str, p: str) -> list[int]:
    """Occurrences of p in text via z-array of p + sentinel + text."""
    if not p:
        return []
    z = z_array(p + "\0" + text)
    return [i - len(p) - 1 for i in range(len(p) + 1, len(z)) if z[i] >= len(p)]


if __name__ == "__main__":
    print(z_array("aabxaab"))
    print(find("xabcabcabc", "abc"))
