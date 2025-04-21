from abc import ABC

from dndbot.battle.expectimax.action import Action
from dndbot.battle.expectimax.actions.damage_data import DamageData
from dndbot.characters.combatant import Combatant


class WeaponAttack(Action, ABC):

    def __init__(self, weapon_type: str, hit: int, damage: list[DamageData]):
        self.weapon_type = weapon_type
        self.hit = hit
        self.damage = damage

    def perform(self, target: Combatant):
        pass

    def average_outcome(self, target: Combatant):
        return sum([d.avg_damage() for d in self.damage])
