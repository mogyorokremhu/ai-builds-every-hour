"""SIR epidemic model, text chart of infected over time. Usage: python epidemic_sir.py [beta] [gamma]"""
import sys


def sir(beta=0.3, gamma=0.1, n=1000.0, i0=1.0, days=160):
    s, i, r = n - i0, i0, 0.0
    out = []
    for _ in range(days):
        new_inf = beta * s * i / n
        new_rec = gamma * i
        s, i, r = s - new_inf, i + new_inf - new_rec, r + new_rec
        out.append((s, i, r))
    return out


if __name__ == "__main__":
    beta = float(sys.argv[1]) if len(sys.argv) > 1 else 0.3
    gamma = float(sys.argv[2]) if len(sys.argv) > 2 else 0.1
    data = sir(beta, gamma)
    peak = max(range(len(data)), key=lambda k: data[k][1])
    print(f"R0={beta / gamma:.1f} peak day {peak} with {data[peak][1]:.0f} infected")
    for day in range(0, len(data), 8):
        print(f"{day:3d} {'#' * int(data[day][1] / 10)}")
