"""Fast matrix exponentiation: Fibonacci numbers and linear recurrences."""


def mat_mul(a, b, mod=None):
    r = [[sum(x * y for x, y in zip(row, col)) for col in zip(*b)] for row in a]
    return [[v % mod for v in row] for row in r] if mod else r


def mat_pow(m, e, mod=None):
    """m**e by repeated squaring."""
    n = len(m)
    result = [[int(i == j) for j in range(n)] for i in range(n)]
    while e:
        if e & 1:
            result = mat_mul(result, m, mod)
        m = mat_mul(m, m, mod)
        e >>= 1
    return result


def fib(n: int, mod=None) -> int:
    return mat_pow([[1, 1], [1, 0]], n, mod)[0][1]


def linear_recurrence(coeffs, init, n, mod=None):
    """n-th term of a(k)=c0*a(k-1)+c1*a(k-2)+... given first len(coeffs) terms."""
    k = len(coeffs)
    if n < k:
        return init[n]
    m = [list(coeffs)] + [[int(j == i) for j in range(k)] for i in range(k - 1)]
    p = mat_pow(m, n - k + 1, mod)
    return sum(p[0][i] * init[k - 1 - i] for i in range(k)) % mod if mod else \
        sum(p[0][i] * init[k - 1 - i] for i in range(k))


if __name__ == "__main__":
    assert [fib(i) for i in range(10)] == [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
    assert fib(90) == 2880067194370816120
    assert linear_recurrence([1, 1], [0, 1], 30) == fib(30)
    assert linear_recurrence([1, 1, 1], [0, 0, 1], 10) == 81  # tribonacci
    print("fib(1000) mod 1e9+7 =", fib(1000, 10**9 + 7))
    print("ok")
