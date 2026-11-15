"""Sliding-window maximum with a monotonic deque. Usage: python monotonic_queue.py"""
from collections import deque


def sliding_max(xs: list[int], k: int) -> list[int]:
    dq: deque[int] = deque()  # indices, values decreasing
    out = []
    for i, x in enumerate(xs):
        while dq and xs[dq[-1]] <= x:
            dq.pop()
        dq.append(i)
        if dq[0] <= i - k:
            dq.popleft()
        if i >= k - 1:
            out.append(xs[dq[0]])
    return out


if __name__ == "__main__":
    data = [1, 3, -1, -3, 5, 3, 6, 7]
    print(data)
    print("window 3 max:", sliding_max(data, 3))
    assert sliding_max(data, 3) == [3, 3, 5, 5, 6, 7]
