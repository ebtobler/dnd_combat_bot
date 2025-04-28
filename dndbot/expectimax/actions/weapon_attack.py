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
        success_state = CombatState(deepcopy(current_state.combatant_states))
        success_state.combatant_states[target].hp -= self.average_damage()
        if success_state.combatant_states[target].hp <= 0:
            success_state.combatant_states[target].hp = 0
        hit_outcome = (chance_of_success, success_state)
        miss_outcome = (1 - chance_of_success, CombatState(deepcopy(current_state.combatant_states)))
        return [hit_outcome, miss_outcome]

    def average_damage(self):
        return sum([d.average_damage() for d in self.damage])

    def hit_chance(self, target: Combatant):
        hit_chance = (20 + 1 - (target.ac - self.hit)) / 20
        if hit_chance < 0.05:
            return 0.05
        elif hit_chance > 0.95:
            return 0.95
        return hit_chance

    def perform(self, target: Combatant, current_state: CombatState, verbose=True):
        attack_roll = next(iter(D20.roll(1))) + self.hit
        if attack_roll >= target.ac:
            if verbose:
                print('Hit!')
            success_state = CombatState(deepcopy(current_state.combatant_states))
            success_state.combatant_states[target].hp -= self.average_damage()
            if success_state.combatant_states[target].hp <= 0:
                success_state.combatant_states[target].hp = 0
            return success_state
        else:
            if verbose:
                print('Miss!')
            return CombatState(current_state.combatant_states)
