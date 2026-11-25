"""Longest common substring via dynamic programming."""


def lcs(a: str, b: str) -> str:
    best, end = 0, 0
    prev = [0] * (len(b) + 1)
    for i in range(1, len(a) + 1):
        cur = [0] * (len(b) + 1)
        for j in range(1, len(b) + 1):
            if a[i - 1] == b[j - 1]:
                cur[j] = prev[j - 1] + 1
                if cur[j] > best:
                    best, end = cur[j], i
        prev = cur
    return a[end - best:end]


if __name__ == "__main__":
    assert lcs("abcdef", "zcdemn") == "cde"
    assert lcs("abc", "xyz") == ""
    print(lcs("interpreter", "preterite"))
    print("ok")
