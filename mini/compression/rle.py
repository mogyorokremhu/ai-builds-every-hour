"""Run-length encoding: compress repeated characters as count+char."""
import re


def encode(s: str) -> str:
    out, i = [], 0
    while i < len(s):
        j = i
        while j < len(s) and s[j] == s[i]:
            j += 1
        out.append(f"{j - i}{s[i]}")
        i = j
    return "".join(out)


def decode(s: str) -> str:
    return "".join(c * int(n) for n, c in re.findall(r"(\d+)(\D)", s))


if __name__ == "__main__":
    text = "WWWWWWWWWWWWBWWWWWWWWWWWWBBBWWWWWWWWWWWWWWWWWWWWWWWWBWWWWWWWWWWWWWW"
    enc = encode(text)
    print(enc)
    assert decode(enc) == text
    print(f"{len(text)} -> {len(enc)} chars")
