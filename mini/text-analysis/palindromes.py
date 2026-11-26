"""Find palindromic words and the longest palindromic substring (Manacher-free expand-around-center)."""
import re


def is_palindrome(s: str) -> bool:
    t = re.sub(r"[^a-z0-9]", "", s.lower())
    return bool(t) and t == t[::-1]


def longest_palindrome(s: str) -> str:
    best = ""
    for c in range(len(s)):
        for lo, hi in ((c, c), (c, c + 1)):
            while lo >= 0 and hi < len(s) and s[lo] == s[hi]:
                lo, hi = lo - 1, hi + 1
            if hi - lo - 1 > len(best):
                best = s[lo + 1:hi]
    return best


def palindromic_words(text: str, min_len: int = 3) -> list[str]:
    words = re.findall(r"[a-z]+", text.lower())
    return sorted({w for w in words if len(w) >= min_len and w == w[::-1]})


if __name__ == "__main__":
    assert is_palindrome("A man, a plan, a canal: Panama")
    assert not is_palindrome("hello")
    assert longest_palindrome("babad") in ("bab", "aba")
    assert longest_palindrome("forgeeksskeegfor") == "geeksskeeg"
    text = "Anna saw a racecar at noon; level heads prevail."
    print(palindromic_words(text))
    print(longest_palindrome("xabacdcabay"))
