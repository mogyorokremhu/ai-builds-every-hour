"""Doubly linked deque with O(1) push/pop at both ends. Usage: python linked_deque.py"""
from __future__ import annotations


class _Node:
    def __init__(self, v):
        self.v, self.prev, self.next = v, None, None


class Deque:
    def __init__(self) -> None:
        self.head = self.tail = None
        self.size = 0

    def push_back(self, v) -> None:
        n = _Node(v)
        if self.tail:
            self.tail.next, n.prev = n, self.tail
        else:
            self.head = n
        self.tail = n
        self.size += 1

    def push_front(self, v) -> None:
        n = _Node(v)
        if self.head:
            self.head.prev, n.next = n, self.head
        else:
            self.tail = n
        self.head = n
        self.size += 1

    def pop_back(self):
        n = self.tail
        if n is None:
            raise IndexError("empty deque")
        self.tail = n.prev
        if self.tail:
            self.tail.next = None
        else:
            self.head = None
        self.size -= 1
        return n.v

    def pop_front(self):
        n = self.head
        if n is None:
            raise IndexError("empty deque")
        self.head = n.next
        if self.head:
            self.head.prev = None
        else:
            self.tail = None
        self.size -= 1
        return n.v

    def __iter__(self):
        n = self.head
        while n:
            yield n.v
            n = n.next


if __name__ == "__main__":
    d = Deque()
    for i in range(3):
        d.push_back(i)
        d.push_front(-i)
    assert list(d) == [-2, -1, 0, 0, 1, 2]
    assert d.pop_front() == -2 and d.pop_back() == 2 and d.size == 4
    print("deque ok:", list(d))
