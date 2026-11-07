"""Generate passwords and passphrases with the `secrets` module, and estimate entropy.

    python passphrase.py                 4 passphrases of 7 words (56 bits)
    python passphrase.py -w 9 -n 2       2 passphrases of 9 words
    python passphrase.py --chars 20      a 20-char random password
    python passphrase.py --check "hunter2"   rough strength estimate
"""
from __future__ import annotations

import argparse
import math
import secrets
import string

# 256 short, distinct, easy-to-type words (8 bits each)
WORDS = """
able acid aged also arch army atom aunt away axis baby back bake ball band bank barn base bath beam
bean bear beef bell belt bend bike bird bite blue boat body bold bolt bone book boot bowl brag brew
cake calm camp cane cape card cart case cave cell chef chin city clam clay clip club coal coat code
coil coin cold cone cook cool cord corn cove crab crew crow cube cult curl dark dart dawn deck deer
desk dial dice dish dock dome door dove drum duck dune dust earl east echo edge envy epic exit face
fact fair fawn fern figs film fire fish five flag flat flax flea foam fold font fork fort frog fuel
gale game gate gear gift glow glue goat gold golf gown grid grin gulf hail half hall harp hawk heat
herb hill hint hive hood hook horn hula idea inch iris iron isle jade jail jazz jeep jest jolt judo
jump jury kale keel kelp kite kiwi knee knot lace lake lamb lamp lane lava lawn leaf lens lily lime
lion loaf lock loft loom lord lute mail malt mane mask maze meal mesh mild mile milk mint mist moat
mole moon moss moth mule myth nail navy neon nest newt node nook nose note oath oboe omen onyx opal
oval oven palm park pear pine plum pond pony pork quay quiz raft rain ramp reed reef rice ring robe
rock roof rope rose ruby rust sage sail salt sand seal seed silk snow sock soup
""".split()
assert len(WORDS) == 256, len(WORDS)


def passphrase(n_words: int, sep: str = "-") -> str:
    return sep.join(secrets.choice(WORDS) for _ in range(n_words))


def password(length: int, symbols: bool = True) -> str:
    alphabet = string.ascii_letters + string.digits + ("!@#$%^&*-_=+?" if symbols else "")
    while True:
        pw = "".join(secrets.choice(alphabet) for _ in range(length))
        # require each class so the result satisfies typical rules
        if (any(c.islower() for c in pw) and any(c.isupper() for c in pw) and any(c.isdigit() for c in pw)
                and (not symbols or any(not c.isalnum() for c in pw))):
            return pw


def estimate_bits(pw: str) -> float:
    """Naive estimate: length * log2(pool size), penalising repeats and sequences."""
    pool = 0
    if any(c.islower() for c in pw):
        pool += 26
    if any(c.isupper() for c in pw):
        pool += 26
    if any(c.isdigit() for c in pw):
        pool += 10
    if any(not c.isalnum() for c in pw):
        pool += 20
    if not pool:
        return 0.0
    effective = len(set(pw)) + 0.5 * (len(pw) - len(set(pw)))
    runs = sum(1 for a, b in zip(pw, pw[1:]) if abs(ord(a) - ord(b)) == 1)
    effective -= 0.5 * runs
    return max(0.0, effective * math.log2(pool))


def verdict(bits: float) -> str:
    for limit, word in ((30, "very weak"), (45, "weak"), (64, "reasonable"), (90, "strong")):
        if bits < limit:
            return word
    return "very strong"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("-w", "--words", type=int, default=7)
    ap.add_argument("-n", "--count", type=int, default=4)
    ap.add_argument("--chars", type=int, default=0, help="make a character password instead")
    ap.add_argument("--no-symbols", action="store_true")
    ap.add_argument("--check", default=None)
    a = ap.parse_args()
    if a.check is not None:
        bits = estimate_bits(a.check)
        print(f"~{bits:.0f} bits — {verdict(bits)}")
        return
    for _ in range(a.count):
        if a.chars:
            pw = password(a.chars, not a.no_symbols)
            bits = a.chars * math.log2(62 + (0 if a.no_symbols else 13))
        else:
            pw = passphrase(a.words)
            bits = a.words * 8
        print(f"{pw:<48} {bits:5.0f} bits  {verdict(bits)}")


if __name__ == "__main__":
    main()
