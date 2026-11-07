"""Word-frequency report with a horizontal bar chart, plus basic text statistics.

    python wordfreq.py FILE [-n 20] [--min-len 3] [--keep-stopwords]
    cat book.txt | python wordfreq.py -
    python wordfreq.py --demo
"""
from __future__ import annotations

import argparse
import re
import sys
from collections import Counter

STOPWORDS = set("""
a an and are as at be but by for from had has have he her his i in is it its me my not of on or our
she so that the their them they this to was we were what when which who will with you your
""".split())

DEMO = """It was the best of times, it was the worst of times, it was the age of wisdom,
it was the age of foolishness, it was the epoch of belief, it was the epoch of incredulity,
it was the season of Light, it was the season of Darkness, it was the spring of hope,
it was the winter of despair."""


def words(text: str) -> list[str]:
    return re.findall(r"[a-z]+(?:'[a-z]+)?", text.lower())


def report(text: str, top: int = 20, min_len: int = 1, keep_stop: bool = False, width: int = 40) -> list[str]:
    all_words = words(text)
    counted = [w for w in all_words if len(w) >= min_len and (keep_stop or w not in STOPWORDS)]
    freq = Counter(counted).most_common(top)
    sentences = [s for s in re.split(r"[.!?]+", text) if s.strip()]
    lines = [
        f"words: {len(all_words)}   unique: {len(set(all_words))}   sentences: {len(sentences)}",
        f"avg word length: {sum(map(len, all_words)) / max(1, len(all_words)):.2f}   "
        f"avg sentence: {len(all_words) / max(1, len(sentences)):.1f} words",
        "",
    ]
    if not freq:
        return lines + ["(no words)"]
    peak = freq[0][1]
    pad = max(len(w) for w, _ in freq)
    for w, c in freq:
        bar = "█" * max(1, round(width * c / peak))
        lines.append(f"{w:>{pad}} {c:>5} {bar}")
    return lines


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("file", nargs="?")
    ap.add_argument("-n", type=int, default=20)
    ap.add_argument("--min-len", type=int, default=1)
    ap.add_argument("--keep-stopwords", action="store_true")
    ap.add_argument("--demo", action="store_true")
    a = ap.parse_args()
    if a.demo or a.file is None:
        text = DEMO
    elif a.file == "-":
        text = sys.stdin.read()
    else:
        with open(a.file, encoding="utf-8", errors="replace") as f:
            text = f.read()
    print("\n".join(report(text, a.n, a.min_len, a.keep_stopwords)))


if __name__ == "__main__":
    main()
