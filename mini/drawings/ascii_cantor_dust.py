"""Cantor set and Cantor dust: 1D set stacked into rows, then a 2D dust square.
python ascii_cantor_dust.py [levels]"""
import sys


def cantor(levels: int) -> list[str]:
    width = 3 ** levels

    def on(x: int, lv: int) -> bool:
        for k in range(lv):  # inspect the top `lv` base-3 digits
            if (x // 3 ** (levels - 1 - k)) % 3 == 1:
                return False
        return True

    return ["".join("█" if on(x, lv) else " " for x in range(width)) for lv in range(levels + 1)]


def dust(levels: int) -> list[str]:
    n = 3 ** levels
    def on(v: int) -> bool:
        while v:
            if v % 3 == 1:
                return False
            v //= 3
        return True
    return ["".join("█" if on(x) and on(y) else " " for x in range(n)) for y in range(n)]


if __name__ == "__main__":
    lv = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    print("\n".join(cantor(lv)))
    print()
    print("\n".join(dust(min(lv, 4))))
