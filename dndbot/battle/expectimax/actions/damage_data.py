from dataclasses import dataclass
from math import floor

from dndbot.dice.dice import Dice


@dataclass
class DamageData:
    dice: tuple[int, Dice]
    mod: int
    dmg_type: str

    def __init__(self, dice: tuple[int, Dice], mod: int, dmg_type: str):
        self.dice = dice
        self.mod = mod
        self.dmg_type = dmg_type

    def roll_damage(self):
        return sum(self.dice[1].roll(self.dice[0])) + self.mod

    def average_damage(self):
        return self.dice[0] * self.dice[1].average_roll + self.mod
