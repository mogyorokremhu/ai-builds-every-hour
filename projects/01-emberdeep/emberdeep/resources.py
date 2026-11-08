"""Torch fuel and hunger: two slowly draining resources that push you ever deeper.

* **Torch** — your light. Its fuel shrinks your field-of-view radius as it burns down;
  when it runs out you only see by the faint glow of embers.
* **Hunger** — satiation drops every turn. When hungry your wounds stop closing while
  waiting; when starving you take damage.
"""
from __future__ import annotations

from dataclasses import dataclass

TORCH_MAX = 1500
FOOD_MAX = 2400

#: (minimum fuel, fov radius, label) — first match wins
TORCH_STAGES: tuple[tuple[int, int, str], ...] = (
    (750, 8, "Bright"),
    (350, 7, "Steady"),
    (120, 5, "Dim"),
    (1, 4, "Guttering"),
    (0, 2, "Out"),
)

#: (minimum satiation, label, colour)
HUNGER_STAGES: tuple[tuple[int, str, str], ...] = (
    (1800, "Full", "bright_green"),
    (400, "Fed", "white"),
    (150, "Hungry", "bright_yellow"),
    (1, "Weak", "bright_red"),
    (0, "Starving", "red"),
)

STARVE_INTERVAL = 8  # turns between starvation damage ticks


def torch_stage(fuel: int) -> tuple[int, str]:
    """The (sight radius, label) of the torch stage for ``fuel``."""
    for minimum, radius, label in TORCH_STAGES:
        if fuel >= minimum:
            return radius, label
    return TORCH_STAGES[-1][1], TORCH_STAGES[-1][2]  # pragma: no cover


def hunger_stage(food: int) -> tuple[str, str]:
    """The (label, colour) of the hunger stage for ``food``."""
    for minimum, label, color in HUNGER_STAGES:
        if food >= minimum:
            return label, color
    return HUNGER_STAGES[-1][1], HUNGER_STAGES[-1][2]  # pragma: no cover


@dataclass
class TickEvents:
    """Messages and damage produced by one resource tick."""

    messages: list[tuple[str, str]]
    starve_damage: int = 0


class Resources:
    """The player's torch fuel and food, which burn down by one each turn."""
    def __init__(self, torch: int = TORCH_MAX, food: int = FOOD_MAX - 200) -> None:
        self.torch = torch
        self.food = food
        self._turns_starving = 0

    @property
    def fov_radius(self) -> int:
        """Sight radius granted by the current torch stage."""
        return torch_stage(self.torch)[0]

    @property
    def torch_label(self) -> str:
        """Label of the current torch stage."""
        return torch_stage(self.torch)[1]

    @property
    def hunger_label(self) -> str:
        """Label of the current hunger stage."""
        return hunger_stage(self.food)[0]

    @property
    def hunger_color(self) -> str:
        """HUD colour of the current hunger stage."""
        return hunger_stage(self.food)[1]

    @property
    def can_regenerate(self) -> bool:
        """Natural healing only works while not hungry."""
        return self.food >= HUNGER_STAGES[1][0]

    def tick(self, turns: int = 1) -> TickEvents:
        """Burn ``turns`` of fuel and food, reporting stage-change messages and starvation damage."""
        events = TickEvents(messages=[])
        for _ in range(turns):
            old_torch, old_food = torch_stage(self.torch)[1], hunger_stage(self.food)[0]
            self.torch = max(0, self.torch - 1)
            self.food = max(0, self.food - 1)
            new_torch, new_food = torch_stage(self.torch)[1], hunger_stage(self.food)[0]
            if new_torch != old_torch:
                events.messages.append(TORCH_MESSAGES[new_torch])
            if new_food != old_food and new_food in HUNGER_MESSAGES:
                events.messages.append(HUNGER_MESSAGES[new_food])
            if self.food == 0:
                self._turns_starving += 1
                if self._turns_starving % STARVE_INTERVAL == 0:
                    events.starve_damage += 1
            else:
                self._turns_starving = 0
        return events

    def refuel(self, amount: int) -> int:
        """Add up to ``amount`` torch fuel (capped at max); return the amount added."""
        added = max(0, min(amount, TORCH_MAX - self.torch))
        self.torch += added
        return added

    def eat(self, amount: int) -> int:
        """Add up to ``amount`` food (capped at max); return the amount added."""
        added = max(0, min(amount, FOOD_MAX - self.food))
        self.food += added
        return added


TORCH_MESSAGES: dict[str, tuple[str, str]] = {
    "Bright": ("Your torch blazes brightly.", "bright_yellow"),
    "Steady": ("Your torch burns lower.", "yellow"),
    "Dim": ("Your torch is growing dim.", "bright_yellow"),
    "Guttering": ("Your torch gutters! Find fuel soon.", "bright_red"),
    "Out": ("Your torch goes out. Darkness closes in.", "bright_red"),
}

HUNGER_MESSAGES: dict[str, tuple[str, str]] = {
    "Fed": ("You no longer feel full.", "white"),
    "Hungry": ("You are getting hungry.", "bright_yellow"),
    "Weak": ("You feel weak with hunger!", "bright_red"),
    "Starving": ("You are starving!", "bright_red"),
}
