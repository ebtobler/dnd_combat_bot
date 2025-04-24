from dataclasses import dataclass

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

    def __repr__(self):
        return f'{self.dice[0]}{str(self.dice[1].__repr__())} + {self.mod} {self.dmg_type}'

    def __str__(self):
        return self.__repr__()

    def __hash__(self):
        return hash(self.dice) + hash(self.mod) + hash(self.dmg_type)

    def roll_damage(self):
        return sum(self.dice[1].roll(self.dice[0])) + self.mod

    def average_damage(self):
        return self.dice[0] * self.dice[1].average_roll + self.mod
