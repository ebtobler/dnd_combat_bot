import unittest
from copy import deepcopy
from unittest import TestCase

from dndbot.characters.combatant import CombatantState
from dndbot.characters.enemies.enemy_character import EnemyCharacter
from dndbot.characters.players.player_character import PlayerCharacter
from dndbot.dice.dice import D6, D12, D8
from dndbot.expectimax.actions.damage_data import DamageData
from dndbot.expectimax.actions.weapon_attack import WeaponAttack
from dndbot.expectimax.combat_state import CombatState
from test._dnd_utils.dnd_utils import DndUtils


class TestCombatState(TestCase):

    def test_health_utility_function_for_single_state(self):
        combatants = [PlayerCharacter({'name': 'p1', 'HP_Max': 10}), PlayerCharacter({'name': 'p2', 'HP_Max': 15}),
                      EnemyCharacter({'name': 'e1', 'HP_Max': 4, 'Initiative': 0}),
                      EnemyCharacter({'name': 'e2', 'HP_Max': 6, 'Initiative': 0})]
        combatant_states = {c: CombatantState(c.name, c.hp_max, c.spell_slot_max) for c in combatants}
        state = CombatState(combatant_states)
        expected_utility = 10 + 15 - 4 - 6
        result = state.health_utility()
        self.assertEqual(expected_utility, result)

    def test_generate_children_with_one_target(self):
        damage = tuple([DamageData((1, D6), 1, 'bludgeoning')])
        player_attack = WeaponAttack('Melee', 4, damage)
        combatants = [PlayerCharacter({'name': 'p1', 'HP_Max': 10, 'Actions': {'Weapon_Attacks': [player_attack]}}),
                      EnemyCharacter({'name': 'e1', 'HP_Max': 4, 'AC': 12, 'Initiative': 0})]
        combatant_states = {c: CombatantState(c.name, c.hp_max, c.spell_slot_max) for c in combatants}
        state = CombatState(combatant_states)

        state.expand_children(combatants[0])
        expected = [player_attack.generate_states(CombatState(combatant_states), combatants[1])]
        self.assertEqual(expected, list(state.children.values()))

    def test_generate_children_with_two_targets(self):
        damage = tuple([DamageData((1, D6), 1, 'bludgeoning')])
        player_attack = WeaponAttack('Melee', 4, damage)
        combatants = [PlayerCharacter({'name': 'p1', 'HP_Max': 10, 'Actions': {'Weapon_Attacks': [player_attack]}}),
                      EnemyCharacter({'name': 'e1', 'HP_Max': 4, 'AC': 12, 'Initiative': 0}),
                      EnemyCharacter({'name': 'e2', 'HP_Max': 4, 'AC': 12, 'Initiative': 0})]
        combatant_states = {c: CombatantState(c.name, c.hp_max, c.spell_slot_max) for c in combatants}
        state = CombatState(combatant_states)

        state.expand_children(combatants[0])
        expected = [player_attack.generate_states(CombatState(combatant_states), combatants[1]),
                    player_attack.generate_states(CombatState(combatant_states), combatants[2])]
        self.assertEqual(expected, list(state.children.values()))

    def test_generate_children_with_two_attacks(self):
        damage_1 = tuple([DamageData((1, D6), 1, 'bludgeoning')])
        player_attack_1 = WeaponAttack('Melee', 4, damage_1)
        damage_2 = tuple([DamageData((1, D12), 1, 'bludgeoning')])
        player_attack_2 = WeaponAttack('Melee', 4, damage_2)

        combatants = [
            PlayerCharacter({
                'name': 'p1',
                'HP_Max': 10,
                'Actions': {
                    'Weapon_Attacks': [player_attack_1, player_attack_2]}
                }),
            EnemyCharacter({'name': 'e1', 'HP_Max': 10, 'AC': 14, 'Initiative': 0}),
            EnemyCharacter({'name': 'e2', 'HP_Max': 4, 'AC': 12, 'Initiative': 0})]
        combatant_states = {c: CombatantState(c.name, c.hp_max, c.spell_slot_max) for c in combatants}
        state = CombatState(combatant_states)

        state.expand_children(combatants[0])
        expected = [player_attack_1.generate_states(CombatState(combatant_states), combatants[1]),
                    player_attack_1.generate_states(CombatState(combatant_states), combatants[2]),
                    player_attack_2.generate_states(CombatState(combatant_states), combatants[1]),
                    player_attack_2.generate_states(CombatState(combatant_states), combatants[2])
                    ]
        self.assertEqual(expected, list(state.children.values()))

    def test_choose_highest_utility_child_when_can_eliminate_one_enemy(self):
        damage_1 = tuple([DamageData((1, D8), 1, 'bludgeoning')])
        player_attack_1 = WeaponAttack('Melee', 6, damage_1)
        damage_2 = tuple([DamageData((1, D12), 2, 'slashing')])
        player_attack_2 = WeaponAttack('Melee', 4, damage_2)

        combatants = [
            PlayerCharacter({
                'name': 'p1',
                'HP_Max': 10,
                'Actions': {
                    'Weapon_Attacks': [player_attack_1, player_attack_2]}
            }),
            EnemyCharacter({'name': 'e1', 'HP_Max': 10, 'AC': 14, 'Initiative': 0}),
            EnemyCharacter({'name': 'e2', 'HP_Max': 5, 'AC': 10, 'Initiative': 0})]
        combatant_states = {c: CombatantState(c.name, c.hp_max, c.spell_slot_max) for c in combatants}
        state = CombatState(combatant_states)

        state.expand_children(combatants[0])
        best_action = state.choose_maximum_utility_child()
        expected = (player_attack_1, combatants[2])
        self.assertEqual(expected, best_action)

    def test_choose_highest_utility_child_when_no_possible_eliminations(self):
        damage_1 = tuple([DamageData((1, D8), 1, 'bludgeoning')])
        player_attack_1 = WeaponAttack('Melee', 6, damage_1)
        damage_2 = tuple([DamageData((1, D12), 2, 'slashing')])
        player_attack_2 = WeaponAttack('Melee', 4, damage_2)

        combatants = [
            PlayerCharacter({
                'name': 'p1',
                'HP_Max': 10,
                'Actions': {
                    'Weapon_Attacks': [player_attack_1, player_attack_2]}
            }),
            EnemyCharacter({'name': 'e1', 'HP_Max': 30, 'AC': 14, 'Initiative': 0}),
            EnemyCharacter({'name': 'e2', 'HP_Max': 25, 'AC': 10, 'Initiative': 0})]
        combatant_states = {c: CombatantState(c.name, c.hp_max, c.spell_slot_max) for c in combatants}
        state = CombatState(combatant_states)

        state.expand_children(combatants[0])
        best_action = state.choose_maximum_utility_child()
        expected = (player_attack_2, combatants[2])
        self.assertEqual(expected, best_action)

    def test_get_child_states(self):
        players, enemies = DndUtils.single_player_and_enemy_one_attack()
        combatant_states = {c: CombatantState(c.name, c.hp_max, c.spell_slot_max) for c in players + enemies}
        state = CombatState(combatant_states)
        state.expand_children(players[0])

        expected = [[(.65, deepcopy(state)), (.35, deepcopy(state))]]
        expected[0][0][1].combatant_states[enemies[0]].hp = 2.5
        for s in expected[0]:
            s[1].children = None
        result = state.get_child_states()
        self.assertEqual(expected, result)

    @unittest.skip('utility function not final')
    def test_utility_with_child_states(self):
        players, enemies = DndUtils.single_player_and_enemy_one_attack()
        combatant_states = {c: CombatantState(c.name, c.hp_max, c.spell_slot_max) for c in players + enemies}
        state = CombatState(combatant_states)
        state.expand_children(players[0])

        result = state.utility()
        expected = .65 * (20 + 5 * 1 - 2.5 - 3 * 1) + .35 * (20 + 5 * 1 - 10 - 3 * 1)

        self.assertEqual(expected, result)
