from copy import deepcopy
from unittest import TestCase

from dndbot.expectimax.actions.damage_data import DamageData
from dndbot.expectimax.actions.weapon_attack import WeaponAttack
from dndbot.expectimax.combat_state import CombatState
from dndbot.characters.combatant import CombatantState
from dndbot.characters.enemies.enemy_character import EnemyCharacter
from dndbot.dice.dice import D6, D4


class TestWeaponAttack(TestCase):

    def test_hit_chance(self):
        attack = WeaponAttack('untyped', 5, tuple([DamageData((1, D6), 1, 'untyped')]))
        target = EnemyCharacter({'AC': 14})
        result = attack.hit_chance(target)
        self.assertEqual(.6, result)

    def test_average_damage(self):
        damage = tuple([DamageData((1, D6), 1, 'untyped'), DamageData((2, D4), 1, 'force')])
        attack = WeaponAttack('untyped', 0, damage)
        result = attack.average_damage()
        expected = 3.5 + 1 + 2.5 * 2 + 1
        self.assertEqual(expected, result)

    def test_generate_states(self):
        damage = tuple([DamageData((1, D6), 1, 'untyped')])
        attack = WeaponAttack('Melee', 4, damage)
        target = EnemyCharacter({'name': 'e1', 'HP_Max': 12, 'AC': 12})
        combatant_state = {target: CombatantState(target.name, target.hp_max, target.spell_slot_max)}
        current_state = CombatState(combatant_state)

        hit_chance = attack.hit_chance(target)
        hit_state = deepcopy(current_state)
        hit_state.combatant_states[target].hp -= 4.5
        miss_chance = 1 - hit_chance
        miss_state = deepcopy(current_state)

        expected = [(hit_chance, hit_state), (miss_chance, miss_state)]
        result = attack.generate_states(current_state, target)
        self.assertEqual(expected, result)

    def test_perform(self):
        pass
