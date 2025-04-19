from abc import ABC, abstractmethod
from collections.abc import MutableMapping
from dataclasses import dataclass


class Combatant(ABC, MutableMapping):
    @abstractmethod
    def roll_initiative(self):
        pass


@dataclass
class CombatantState:
    name: str
    hp: int
    spell_slots: dict[int: int]

    def __init__(self, name, hp, spell_slots):
        self.name = name
        self.hp = hp
        self.spell_slots = spell_slots
