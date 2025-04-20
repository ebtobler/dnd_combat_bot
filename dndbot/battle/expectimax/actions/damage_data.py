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
