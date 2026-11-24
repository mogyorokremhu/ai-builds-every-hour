#!/usr/bin/env python3
"""Convert integers to English words: `num2words.py 1234` -> one thousand two hundred thirty-four."""
import sys

ONES = "zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen".split()
TENS = "_ _ twenty thirty forty fifty sixty seventy eighty ninety".split()
SCALES = ["", "thousand", "million", "billion", "trillion"]


def below_thousand(n: int) -> str:
    parts = []
    if n >= 100:
        parts.append(ONES[n // 100] + " hundred")
        n %= 100
    if n >= 20:
        parts.append(TENS[n // 10] + ("-" + ONES[n % 10] if n % 10 else ""))
    elif n or not parts:
        parts.append(ONES[n])
    return " ".join(parts)


def to_words(n: int) -> str:
    if n < 0:
        return "minus " + to_words(-n)
    if n == 0:
        return "zero"
    chunks = []
    i = 0
    while n:
        n, r = divmod(n, 1000)
        if r:
            chunks.append(below_thousand(r) + (" " + SCALES[i] if SCALES[i] else ""))
        i += 1
    return " ".join(reversed(chunks))


def selftest() -> None:
    assert to_words(0) == "zero"
    assert to_words(21) == "twenty-one"
    assert to_words(100) == "one hundred"
    assert to_words(1234) == "one thousand two hundred thirty-four"
    assert to_words(-5) == "minus five"
    assert to_words(1000001) == "one million one"
    print("ok")


if __name__ == "__main__":
    args = sys.argv[1:]
    if args == ["--selftest"] or not args:
        selftest()
    else:
        for a in args:
            print(to_words(int(a)))
