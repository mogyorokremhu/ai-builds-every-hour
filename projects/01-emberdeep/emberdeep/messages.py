"""A bounded, colour-aware message log with stacking of repeats."""
from __future__ import annotations

from collections import deque
from dataclasses import dataclass


@dataclass
class Message:
    text: str
    color: str = "white"
    count: int = 1
    turn: int = 0

    @property
    def full_text(self) -> str:
        return f"{self.text} (x{self.count})" if self.count > 1 else self.text


class MessageLog:
    def __init__(self, capacity: int = 200) -> None:
        self._msgs: deque[Message] = deque(maxlen=capacity)

    def add(self, text: str, color: str = "white", turn: int = 0) -> None:
        # Stack identical consecutive messages: "The rat bites you. (x3)"
        if self._msgs and self._msgs[-1].text == text:
            self._msgs[-1].count += 1
            self._msgs[-1].turn = turn
        else:
            self._msgs.append(Message(text, color, 1, turn))

    def last(self, n: int) -> list[str]:
        return [m.full_text for m in list(self._msgs)[-n:]] if n > 0 else []

    def entries(self, n: int | None = None) -> list[Message]:
        msgs = list(self._msgs)
        return msgs if n is None else msgs[-n:] if n > 0 else []

    def __len__(self) -> int:
        return len(self._msgs)


def a_an(name: str) -> str:
    """Prefix a noun with the right indefinite article: 'an ember imp', 'a rat'."""
    return f"{'an' if name[:1].lower() in 'aeiou' else 'a'} {name}"
