from abc import ABC
from typing import Callable

from dndbot.battle.expectimax.action import Action


class WeaponAttack(Action, ABC):

    def __init__(self, weapon_type: str, hit: int, damage: list[tuple[int, Callable[[int], list[int]]]]):
        self.weapon_type = weapon_type
        self.hit = hit
        self.damage = damage

    def perform(self):
        pass
