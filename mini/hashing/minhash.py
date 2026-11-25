"""MinHash: estimate Jaccard similarity of two sets from small signatures."""
import random

P = (1 << 61) - 1


def signature(items, coeffs):
    hs = [hash(x) & 0xFFFFFFFF for x in items]
    return [min((a * h + b) % P for h in hs) for a, b in coeffs]


def estimate(sig_a, sig_b) -> float:
    return sum(x == y for x, y in zip(sig_a, sig_b)) / len(sig_a)


if __name__ == "__main__":
    rng = random.Random(1)
    coeffs = [(rng.randrange(1, P), rng.randrange(P)) for _ in range(256)]
    a = set(range(0, 100))
    b = set(range(50, 150))
    true = len(a & b) / len(a | b)
    est = estimate(signature(a, coeffs), signature(b, coeffs))
    print(f"true Jaccard {true:.3f}, MinHash estimate {est:.3f}")
    assert abs(true - est) < 0.12
