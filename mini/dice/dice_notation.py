"""Parse and roll dice notation like '3d6+2', '2d8-1', '4d6kh3' (keep highest)."""
import random
import re
import sys

PATTERN = re.compile(r"^(\d*)d(\d+)(?:k([hl])(\d+))?([+-]\d+)?$")


def roll(spec: str, rng: random.Random | None = None) -> tuple[int, list[int]]:
    """Roll `spec`; return (total, kept dice)."""
    rng = rng or random.Random()
    m = PATTERN.match(spec.replace(" ", "").lower())
    if not m:
        raise ValueError(f"bad dice spec: {spec!r}")
    n = int(m.group(1) or 1)
    sides = int(m.group(2))
    dice = [rng.randint(1, sides) for _ in range(n)]
    if m.group(3):
        keep = int(m.group(4))
        dice = sorted(dice, reverse=m.group(3) == "h")[:keep]
    return sum(dice) + int(m.group(5) or 0), dice


if __name__ == "__main__":
    for spec in sys.argv[1:] or ["3d6+2", "4d6kh3", "d20"]:
        total, dice = roll(spec)
        print(f"{spec}: {total}  {dice}")
