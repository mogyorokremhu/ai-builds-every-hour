"""Check Zipf's law: fit log(freq) ~ a + b*log(rank) by least squares."""
import math
import re
from collections import Counter


def zipf_slope(text: str) -> float:
    """Return the slope of log-frequency vs log-rank (about -1 for natural text)."""
    freqs = sorted(Counter(re.findall(r"[a-z']+", text.lower())).values(), reverse=True)
    xs = [math.log(r) for r in range(1, len(freqs) + 1)]
    ys = [math.log(f) for f in freqs]
    n = len(xs)
    if n < 2:
        return 0.0
    mx, my = sum(xs) / n, sum(ys) / n
    den = sum((x - mx) ** 2 for x in xs)
    return sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / den


if __name__ == "__main__":
    names = ["w" + "".join(chr(97 + int(d)) for d in str(i)) for i in range(1, 65)]
    synthetic = " ".join((n + " ") * max(1, 64 // i) for i, n in enumerate(names, 1))
    s = zipf_slope(synthetic)
    assert -1.5 < s < -0.5, s
    assert zipf_slope("one") == 0.0
    print("slope: %.2f" % s)
