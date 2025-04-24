from abc import abstractmethod
from dataclasses import dataclass
from typing import Protocol, runtime_checkable


@runtime_checkable
class Combatant(Protocol):

    team: str
    name: str
    hp_max: int
    ac: int
    initiative: int
    speed: int
    ability_scores: dict[str, int]
    saving_throws: dict[str, int]
    actions: dict[str, list['Action']]
    spells: dict[str, str]
    spell_slot_max: dict[str, int]

    @abstractmethod
    def roll_initiative(self):
        pass


@dataclass
class CombatantState:
    name: str
    hp: int
    spell_slots: dict[int: int]

    def __init__(self, name: str, hp: int, spell_slots: dict[int: int]):
        self.name = name
        self.hp = hp
        self.spell_slots = spell_slots

    def __repr__(self):
        return str(self.hp) + ' hp'
