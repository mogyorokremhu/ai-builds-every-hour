"""Happy numbers: repeatedly sum the squares of digits; do we reach 1?"""
import sys


def step(n: int) -> int:
    return sum(int(d) ** 2 for d in str(n))


def chain(n: int):
    seen, out = set(), [n]
    while n != 1 and n not in seen:
        seen.add(n)
        n = step(n)
        out.append(n)
    return out


def is_happy(n: int) -> bool:
    return chain(n)[-1] == 1


if __name__ == "__main__":
    limit = int(sys.argv[1]) if len(sys.argv) > 1 else 100
    happy = [n for n in range(1, limit + 1) if is_happy(n)]
    print(f"{len(happy)} happy numbers up to {limit}:", *happy)
    print("chain for 4:", " -> ".join(map(str, chain(4))))
    print("chain for 19:", " -> ".join(map(str, chain(19))))
