"""Net turning angle of an L-system path: counts of + and -, final heading, closed-loop check."""
from expand import expand


def net_turn(s: str, angle: float) -> float:
    return (s.count("+") - s.count("-")) * angle


if __name__ == "__main__":
    tests = [
        ("koch", "F", {"F": "F+F-F-F+F"}, 90.0),
        ("snowflake", "F--F--F", {"F": "F+F--F+F"}, 60.0),
        ("sierpinski", "F-G-G", {"F": "F-G+F+G-F", "G": "GG"}, 120.0),
    ]
    for name, axiom, rules, ang in tests:
        for g in range(4):
            s = expand(axiom, rules, g)
            t = net_turn(s, ang) % 360
            print(f"{name:10} gen {g}: +={s.count('+'):4d} -={s.count('-'):4d} net={t:6.1f} deg closed_heading={t == 0 or abs(t - 360) < 1e-9}")
