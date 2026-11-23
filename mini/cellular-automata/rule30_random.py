"""Use Rule 30's centre column as a pseudo-random bit stream and print bytes / a coin-flip histogram."""
import sys


def rule30_bits(n: int) -> list:
    width = 2 * n + 3
    row = [0] * width
    row[width // 2] = 1
    out = []
    for _ in range(n):
        out.append(row[width // 2])
        row = [row[i - 1] ^ (row[i] | row[(i + 1) % width]) for i in range(width)]
    return out


def to_bytes(bits: list) -> list:
    return [int("".join(map(str, bits[i:i + 8])), 2) for i in range(0, len(bits) - 7, 8)]


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 256
    bits = rule30_bits(n)
    print("bytes:", to_bytes(bits)[:16])
    print(f"ones: {sum(bits)}/{n} ({100 * sum(bits) / n:.1f}%)")
    runs, cur = {}, 1
    for a, b in zip(bits, bits[1:]):
        if a == b:
            cur += 1
        else:
            runs[cur] = runs.get(cur, 0) + 1
            cur = 1
    runs[cur] = runs.get(cur, 0) + 1
    for k in sorted(runs):
        print(f"run {k}: {'#' * min(runs[k], 60)} {runs[k]}")
