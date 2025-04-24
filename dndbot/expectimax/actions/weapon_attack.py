from abc import ABC
from copy import deepcopy

from dndbot.dice.dice import D20
from dndbot.expectimax.action import Action
from dndbot.expectimax.actions.damage_data import DamageData
from dndbot.expectimax.combat_state import CombatState
from dndbot.characters.combatant import Combatant


class WeaponAttack(Action, ABC):

    def __init__(self, weapon_type: str, hit: int, damage: tuple[DamageData]):
        self.weapon_type = weapon_type
        self.hit = hit
        self.damage = damage
        self.hit_state = None
        self.miss_state = None

    def __eq__(self, other):
        return isinstance(other, WeaponAttack) \
               and self.weapon_type == other.weapon_type \
               and self.hit == other.hit \
               and self.damage == other.damage

    def __repr__(self):
        return f'{self.weapon_type} Weapon Attack: {self.hit} to hit. Hit: {self.damage} damage'

    def __hash__(self):
        return hash(self.weapon_type) + hash(self.hit) + hash(self.damage)

    def generate_states(self, current_state: CombatState, target: Combatant):
        chance_of_success = self.hit_chance(target)
        success_state = deepcopy(current_state)
        success_state.combatant_states[target].hp -= self.average_damage()
        if success_state.combatant_states[target].hp <= 0:
            success_state.combatant_states[target].hp = 0
        hit_outcome = (chance_of_success, success_state)
        miss_outcome = (1 - chance_of_success, deepcopy(current_state))
        self.hit_state = hit_outcome
        self.miss_state = miss_outcome
        return [hit_outcome, miss_outcome]

    def average_damage(self):
        return sum([d.average_damage() for d in self.damage])

    def hit_chance(self, target: Combatant):
        hit_chance = 1 - (target.ac - self.hit - 1) / 20
        if hit_chance < 0.05:
            return 0.05
        elif hit_chance > 0.95:
            return 0.95
        return hit_chance

    def perform(self, target: Combatant):
        assert(self.hit_state is not None and self.miss_state is not None)
        attack_roll = next(iter(D20.roll(1))) + self.hit
        if attack_roll >= target.ac:
            return self.hit_state
        else:
            return self.miss_state
