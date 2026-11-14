"""Fixed-size ring buffer with overwrite. Usage: python ring_buffer.py"""


class RingBuffer:
    def __init__(self, capacity: int) -> None:
        if capacity < 1:
            raise ValueError("capacity must be >= 1")
        self.buf = [None] * capacity
        self.start = 0
        self.count = 0

    def push(self, item) -> None:
        """Append; overwrites the oldest item when full."""
        cap = len(self.buf)
        self.buf[(self.start + self.count) % cap] = item
        if self.count < cap:
            self.count += 1
        else:
            self.start = (self.start + 1) % cap

    def pop(self):
        """Remove and return the oldest item."""
        if not self.count:
            raise IndexError("pop from empty buffer")
        item = self.buf[self.start]
        self.buf[self.start] = None
        self.start = (self.start + 1) % len(self.buf)
        self.count -= 1
        return item

    def __len__(self) -> int:
        return self.count

    def __iter__(self):
        for i in range(self.count):
            yield self.buf[(self.start + i) % len(self.buf)]


if __name__ == "__main__":
    r = RingBuffer(3)
    for i in range(1, 6):
        r.push(i)
    assert list(r) == [3, 4, 5]
    assert r.pop() == 3 and list(r) == [4, 5]
    print("ring buffer ok:", list(r))
