"""Stack with O(1) push/pop/min. Usage: python min_stack.py"""


class MinStack:
    def __init__(self):
        self._items: list[tuple[int, int]] = []

    def push(self, x: int) -> None:
        m = min(x, self._items[-1][1]) if self._items else x
        self._items.append((x, m))

    def pop(self) -> int:
        return self._items.pop()[0]

    def peek(self) -> int:
        return self._items[-1][0]

    def minimum(self) -> int:
        return self._items[-1][1]

    def __len__(self) -> int:
        return len(self._items)


if __name__ == "__main__":
    s = MinStack()
    for x in [5, 3, 7, 2, 8]:
        s.push(x)
        print(f"push {x}: min={s.minimum()}")
    while len(s):
        print(f"pop {s.pop()}: remaining={len(s)}", f"min={s.minimum()}" if len(s) else "")
