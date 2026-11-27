"""Net present value and internal rate of return (bisection)."""


def npv(rate: float, flows: list[float]) -> float:
    """flows[0] occurs now; flows[t] at the end of period t."""
    return sum(cf / (1 + rate) ** t for t, cf in enumerate(flows))


def irr(flows: list[float], lo: float = -0.99, hi: float = 10.0) -> float:
    """Rate where NPV is zero; needs a sign change between lo and hi."""
    if npv(lo, flows) * npv(hi, flows) > 0:
        raise ValueError("no sign change: IRR not bracketed")
    for _ in range(200):
        mid = (lo + hi) / 2
        if npv(lo, flows) * npv(mid, flows) <= 0:
            hi = mid
        else:
            lo = mid
    return (lo + hi) / 2


if __name__ == "__main__":
    flows = [-1000, 300, 400, 500, 200]
    print(f"NPV @8%: {npv(0.08, flows):.2f}")
    r = irr(flows)
    print(f"IRR: {r:.4%}")
    assert abs(npv(r, flows)) < 1e-6
