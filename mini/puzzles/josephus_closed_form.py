"""Josephus problem: simulation vs recurrence vs the power-of-two closed form (k=2)."""


def simulate(n: int, k: int) -> int:
    people = list(range(1, n + 1))
    i = 0
    while len(people) > 1:
        i = (i + k - 1) % len(people)
        people.pop(i)
    return people[0]


def recurrence(n: int, k: int) -> int:
    r = 0
    for m in range(2, n + 1):
        r = (r + k) % m
    return r + 1


def closed_form_k2(n: int) -> int:
    p = 1 << (n.bit_length() - 1)
    return 2 * (n - p) + 1


if __name__ == "__main__":
    for n in range(1, 60):
        for k in (2, 3, 5):
            assert simulate(n, k) == recurrence(n, k)
        assert simulate(n, 2) == closed_form_k2(n)
    print("n=41,k=3 survivor:", recurrence(41, 3))
