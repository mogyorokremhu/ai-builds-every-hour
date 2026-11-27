"""RAKE-style keyword extraction: split on stopwords, score phrases by degree/frequency."""
import re
from collections import defaultdict

STOP = set("a an the and or of to in on for with is are was were be by as at it this that from over into".split())


def rake(text: str, top: int = 5) -> list[tuple[str, float]]:
    """Return the top-scoring candidate phrases."""
    words = re.findall(r"[a-z']+|[.,;!?]", text.lower())
    phrases, cur = [], []
    for w in words:
        if w in STOP or not w[0].isalpha():
            if cur:
                phrases.append(cur)
            cur = []
        else:
            cur.append(w)
    if cur:
        phrases.append(cur)
    freq: dict[str, int] = defaultdict(int)
    deg: dict[str, int] = defaultdict(int)
    for p in phrases:
        for w in p:
            freq[w] += 1
            deg[w] += len(p)
    scored = {" ".join(p): sum(deg[w] / freq[w] for w in p) for p in phrases}
    return sorted(scored.items(), key=lambda kv: (-kv[1], kv[0]))[:top]


if __name__ == "__main__":
    r = rake("Compatibility of systems of linear constraints over the set of natural numbers.")
    assert r[0][0] == "linear constraints", r
    for ph, sc in r:
        print("%5.1f  %s" % (sc, ph))
