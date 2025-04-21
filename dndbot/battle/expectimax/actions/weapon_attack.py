from abc import ABC

from dndbot.battle.expectimax.action import Action
from dndbot.battle.expectimax.actions.damage_data import DamageData
from dndbot.characters.combatant import Combatant


class WeaponAttack(Action, ABC):

    def __init__(self, weapon_type: str, hit: int, damage: list[DamageData]):
        self.weapon_type = weapon_type
        self.hit = hit
        self.damage = damage

    def __eq__(self, other):
        return isinstance(other, WeaponAttack) \
               and self.weapon_type == other.weapon_type \
               and self.hit == other.hit \
               and self.damage == other.damage

    def perform(self, target: Combatant):
        pass

    def average_outcome(self, target: Combatant):
        return sum([d.average_damage() for d in self.damage])
