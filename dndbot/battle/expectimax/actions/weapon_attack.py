from abc import ABC

from dndbot.battle.expectimax.action import Action
from dndbot.battle.expectimax.actions.damage_data import DamageData
from dndbot.characters.combatant import CombatantState, Combatant


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

    def perform(self, target: CombatantState):
        pass

    def average_outcome(self, target: Combatant):
        return self.hit_chance(target) * self.average_damage()

    def average_damage(self):
        return sum([d.average_damage() for d in self.damage])

    def hit_chance(self, target: Combatant):
        hit_chance = (target.ac - self.hit) * 0.05
        if hit_chance < 0.05:
            return 0.05
        elif hit_chance > 0.95:
            return 0.95
        return hit_chance
