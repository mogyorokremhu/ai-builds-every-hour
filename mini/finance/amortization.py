"""Loan amortization schedule. Usage: python amortization.py [principal] [annual_rate_pct] [years]"""
import sys


def payment(principal: float, annual_pct: float, years: int) -> float:
    """Fixed monthly payment for a fully amortizing loan."""
    n = years * 12
    r = annual_pct / 100 / 12
    if r == 0:
        return principal / n
    return principal * r / (1 - (1 + r) ** -n)


def schedule(principal: float, annual_pct: float, years: int):
    """Yield (month, payment, interest, principal_paid, balance) rows."""
    pay = payment(principal, annual_pct, years)
    r = annual_pct / 100 / 12
    bal = principal
    for m in range(1, years * 12 + 1):
        interest = bal * r
        princ = pay - interest
        bal = max(0.0, bal - princ)
        yield m, pay, interest, princ, bal


def main(argv: list[str]) -> None:
    p = float(argv[1]) if len(argv) > 1 else 200000
    rate = float(argv[2]) if len(argv) > 2 else 5.0
    yrs = int(argv[3]) if len(argv) > 3 else 15
    print(f"Loan {p:,.0f} at {rate}% for {yrs} years")
    total_int = 0.0
    print(f"{'Mo':>4} {'Payment':>10} {'Interest':>10} {'Principal':>10} {'Balance':>12}")
    for m, pay, i, pr, b in schedule(p, rate, yrs):
        total_int += i
        if m <= 3 or m % 12 == 0:
            print(f"{m:>4} {pay:>10.2f} {i:>10.2f} {pr:>10.2f} {b:>12.2f}")
    print(f"Total interest: {total_int:,.2f}")


if __name__ == "__main__":
    main(sys.argv)
