from abc import ABC
from copy import deepcopy

from dndbot.battle.expectimax.action import Action
from dndbot.battle.expectimax.actions.damage_data import DamageData
from dndbot.battle.expectimax.expectimax import CombatState
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

    def generate_states(self, current_state: CombatState, target: Combatant):
        chance_of_success = self.hit_chance(target)
        success_state = deepcopy(current_state)
        success_state.combatant_states[target].hp -= self.average_damage()
        hit_outcome = (chance_of_success, success_state)
        miss_outcome = (1 - chance_of_success, deepcopy(current_state))
        return self, [hit_outcome, miss_outcome]

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
