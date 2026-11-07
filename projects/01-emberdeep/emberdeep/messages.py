"""A bounded message log shown under the map."""
from __future__ import annotations

from collections import deque


class MessageLog:
    def __init__(self, capacity: int = 100) -> None:
        self._msgs: deque[str] = deque(maxlen=capacity)

    def add(self, text: str) -> None:
        # Stack identical consecutive messages: "The rat bites you. (x3)"
        if self._msgs and self._msgs[-1].split(" (x")[0] == text:
            last = self._msgs.pop()
            count = int(last.split(" (x")[1][:-1]) + 1 if " (x" in last else 2
            self._msgs.append(f"{text} (x{count})")
        else:
            self._msgs.append(text)

    def last(self, n: int) -> list[str]:
        return list(self._msgs)[-n:]

    def __len__(self) -> int:
        return len(self._msgs)
