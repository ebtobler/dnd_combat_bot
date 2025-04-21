from dataclasses import dataclass
from typing import Callable


@dataclass
class DamageData:
    dice: tuple[int, Callable[[int], list[int]]]
    mod: int
    dmg_type: str

    def __init__(self, dice: tuple[int, Callable[[int], list[int]]], mod: int, dmg_type: str):
        self.dice = dice
        self.mod = mod
        self.dmg_type = dmg_type

    def roll_damage(self):
        return sum(self.dice[1](self.dice[0]) + self.dice[2])  # dx(n) + mod

    def avg_damage(self):
        pass
