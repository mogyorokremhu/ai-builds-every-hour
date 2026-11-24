"""Word frequency counter with a simple text bar chart."""
import re
from collections import Counter


def word_freq(text: str, top: int = 5) -> list[tuple[str, int]]:
    """Return the `top` most common lowercase words."""
    return Counter(re.findall(r"[a-z']+", text.lower())).most_common(top)


if __name__ == "__main__":
    sample = "the cat and the hat and the bat sat on the mat"
    res = word_freq(sample, 3)
    assert res[0] == ("the", 4) and res[1] == ("and", 2)
    for w, n in res:
        print(f"{w:>6} {'#' * n} {n}")
