"""Generate plausible license plates in several national-style formats.
Usage: python license_plate.py [count] [seed]"""
import random
import string
import sys

FORMATS = {"EU": "LLL-DDD", "UK": "LLDD LLL", "HU": "LLL-DDD", "US": "DLLL DDD"}


def plate(fmt: str, rng: random.Random) -> str:
    """Fill a format string: L = letter, D = digit, others literal."""
    out = []
    for ch in fmt:
        if ch == "L":
            out.append(rng.choice(string.ascii_uppercase))
        elif ch == "D":
            out.append(rng.choice(string.digits))
        else:
            out.append(ch)
    return "".join(out)


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    rng = random.Random(int(sys.argv[2]) if len(sys.argv) > 2 else None)
    for country, fmt in FORMATS.items():
        print(country, " ".join(plate(fmt, rng) for _ in range(n)))
