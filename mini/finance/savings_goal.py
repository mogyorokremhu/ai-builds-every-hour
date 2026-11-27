"""Monthly deposit needed to reach a savings goal (annuity formula)."""


def monthly_deposit(goal: float, annual_pct: float, years: int, start: float = 0.0) -> float:
    n = years * 12
    i = annual_pct / 100 / 12
    if i == 0:
        return (goal - start) / n
    growth = (1 + i) ** n
    return (goal - start * growth) * i / (growth - 1)


if __name__ == "__main__":
    d = monthly_deposit(50000, 5, 10, start=2000)
    print(f"Deposit per month: {d:.2f}")
    # verify by simulation
    bal = 2000.0
    for _ in range(120):
        bal = bal * (1 + 0.05 / 12) + d
    assert abs(bal - 50000) < 1e-6
    print(f"Final balance: {bal:.2f}")
