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

    def roll_damage(self):
        pass  # dx(n) + mod

    def avg_damage(self):
        pass
