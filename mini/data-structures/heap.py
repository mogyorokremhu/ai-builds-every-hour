"""Binary min-heap from scratch. Usage: python heap.py  (runs a heap-sort demo)."""
import random
from typing import Generic, List, TypeVar

T = TypeVar("T")


class MinHeap(Generic[T]):
    """Array-backed binary min-heap."""

    def __init__(self) -> None:
        self.a: List[T] = []

    def __len__(self) -> int:
        return len(self.a)

    def push(self, x: T) -> None:
        a = self.a
        a.append(x)
        i = len(a) - 1
        while i > 0 and a[(i - 1) // 2] > a[i]:
            a[(i - 1) // 2], a[i] = a[i], a[(i - 1) // 2]
            i = (i - 1) // 2

    def pop(self) -> T:
        a = self.a
        top, last = a[0], a.pop()
        if a:
            a[0] = last
            i = 0
            while True:
                c = 2 * i + 1
                if c >= len(a):
                    break
                if c + 1 < len(a) and a[c + 1] < a[c]:
                    c += 1
                if a[i] <= a[c]:
                    break
                a[i], a[c] = a[c], a[i]
                i = c
        return top


def heap_sort(xs):
    h = MinHeap()
    for x in xs:
        h.push(x)
    return [h.pop() for _ in range(len(h))]


if __name__ == "__main__":
    data = [random.randint(0, 99) for _ in range(15)]
    print("input :", data)
    print("sorted:", heap_sort(data))
    assert heap_sort(data) == sorted(data)
