"""Perfect, abundant and deficient numbers plus amicable pairs below N."""
import sys


def divisor_sums(limit: int) -> list[int]:
    """Sum of proper divisors for every n < limit (sieve style)."""
    s = [0] * limit
    for d in range(1, limit // 2 + 1):
        for m in range(2 * d, limit, d):
            s[m] += d
    return s


if __name__ == "__main__":
    limit = int(sys.argv[1]) if len(sys.argv) > 1 else 10000
    s = divisor_sums(limit)
    perfect = [n for n in range(2, limit) if s[n] == n]
    abundant = sum(1 for n in range(2, limit) if s[n] > n)
    amicable = [(a, s[a]) for a in range(2, limit) if a < s[a] < limit and s[s[a]] == a]
    print("perfect:", perfect)
    print("abundant count:", abundant, " deficient count:", limit - 2 - abundant - len(perfect))
    print("amicable pairs:", amicable)
