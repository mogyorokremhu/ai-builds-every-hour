"""Bounded-buffer producer/consumer with counting semaphores (deterministic simulation)."""
from collections import deque


class Semaphore:
    def __init__(self, value):
        self.value = value
        self.waiting = deque()


def simulate(buffer_size=2, items=6):
    """Round-robin one step per process; returns the event log."""
    empty, full = Semaphore(buffer_size), Semaphore(0)
    buf, log = deque(), []
    produced = consumed = 0
    for _ in range(items * 6):
        if produced < items and empty.value > 0:
            empty.value -= 1
            buf.append(produced)
            log.append(f"P put {produced} {list(buf)}")
            produced += 1
            full.value += 1
        elif produced < items:
            log.append("P blocked (buffer full)")
        if consumed < items and full.value > 0:
            full.value -= 1
            x = buf.popleft()
            log.append(f"C got {x} {list(buf)}")
            consumed += 1
            empty.value += 1
        elif consumed < items:
            log.append("C blocked (buffer empty)")
        if consumed == items:
            break
    assert consumed == items and not buf
    return log


if __name__ == "__main__":
    print("\n".join(simulate()))
