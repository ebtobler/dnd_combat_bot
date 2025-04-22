from unittest import TestCase

from dndbot.battle.expectimax.actions.damage_data import DamageData
from dndbot.battle.expectimax.actions.weapon_attack import WeaponAttack
from dndbot.battle.expectimax.expectimax import CombatState
from dndbot.characters.combatant import CombatantState
from dndbot.characters.enemies.enemy_character import EnemyCharacter
from dndbot.characters.players.player_character import PlayerCharacter
from dndbot.dice.dice import D6, D12, D8, D4


class TestCombatState(TestCase):

    def test_health_utility_function_for_single_state(self):
        combatants = [PlayerCharacter({'name': 'p1', 'HP_Max': 10}), PlayerCharacter({'name': 'p2', 'HP_Max': 15}),
                      EnemyCharacter({'name': 'e1', 'HP_Max': 4}), EnemyCharacter({'name': 'e2', 'HP_Max': 6})]
        combatant_states = {c: CombatantState(c.name, c.hp_max, c.spell_slot_max) for c in combatants}
        state = CombatState(combatant_states)
        expected_utility = 10 + 15 - 4 - 6
        result = state.health_utility()
        self.assertEqual(expected_utility, result)

    def test_generate_children_with_one_target(self):
        damage = [DamageData((1, D6), 1, 'bludgeoning')]
        player_attack = WeaponAttack('Melee', 4, damage)
        combatants = [PlayerCharacter({'name': 'p1', 'HP_Max': 10, 'Actions': {'Weapon_Attacks': [player_attack]}}),
                      EnemyCharacter({'name': 'e1', 'HP_Max': 4, 'AC': 12})]
        combatant_states = {c: CombatantState(c.name, c.hp_max, c.spell_slot_max) for c in combatants}
        state = CombatState(combatant_states)

        state.generate_children(combatants[0])
        expected = [player_attack.generate_states(CombatState(combatant_states), combatants[1])]
        self.assertEqual(expected, state.children)

    def test_generate_children_with_two_targets(self):
        damage = [DamageData((1, D6), 1, 'bludgeoning')]
        player_attack = WeaponAttack('Melee', 4, damage)
        combatants = [PlayerCharacter({'name': 'p1', 'HP_Max': 10, 'Actions': {'Weapon_Attacks': [player_attack]}}),
                      EnemyCharacter({'name': 'e1', 'HP_Max': 4, 'AC': 12}),
                      EnemyCharacter({'name': 'e2', 'HP_Max': 4, 'AC': 12})]
        combatant_states = {c: CombatantState(c.name, c.hp_max, c.spell_slot_max) for c in combatants}
        state = CombatState(combatant_states)

        state.generate_children(combatants[0])
        expected = [player_attack.generate_states(CombatState(combatant_states), combatants[1]),
                    player_attack.generate_states(CombatState(combatant_states), combatants[2])]
        self.assertEqual(expected, state.children)

    def test_generate_children_with_two_attacks(self):
        damage_1 = [DamageData((1, D6), 1, 'bludgeoning')]
        player_attack_1 = WeaponAttack('Melee', 4, damage_1)
        damage_2 = [DamageData((1, D12), 1, 'bludgeoning')]
        player_attack_2 = WeaponAttack('Melee', 4, damage_2)

        combatants = [
            PlayerCharacter({
                'name': 'p1',
                'HP_Max': 10,
                'Actions': {
                    'Weapon_Attacks': [player_attack_1, player_attack_2]}
                }),
            EnemyCharacter({'name': 'e1', 'HP_Max': 10, 'AC': 14}),
            EnemyCharacter({'name': 'e2', 'HP_Max': 4, 'AC': 12})]
        combatant_states = {c: CombatantState(c.name, c.hp_max, c.spell_slot_max) for c in combatants}
        state = CombatState(combatant_states)

        state.generate_children(combatants[0])
        expected = [player_attack_1.generate_states(CombatState(combatant_states), combatants[1]),
                    player_attack_1.generate_states(CombatState(combatant_states), combatants[2]),
                    player_attack_2.generate_states(CombatState(combatant_states), combatants[1]),
                    player_attack_2.generate_states(CombatState(combatant_states), combatants[2])
                    ]
        self.assertEqual(expected, state.children)

    def test_choose_highest_utility_child_when_can_eliminate_one_enemy(self):
        damage_1 = [DamageData((1, D8), 1, 'bludgeoning')]
        player_attack_1 = WeaponAttack('Melee', 6, damage_1)
        damage_2 = [DamageData((1, D12), 2, 'slashing')]
        player_attack_2 = WeaponAttack('Melee', 4, damage_2)

        combatants = [
            PlayerCharacter({
                'name': 'p1',
                'HP_Max': 10,
                'Actions': {
                    'Weapon_Attacks': [player_attack_1, player_attack_2]}
            }),
            EnemyCharacter({'name': 'e1', 'HP_Max': 10, 'AC': 14}),
            EnemyCharacter({'name': 'e2', 'HP_Max': 5, 'AC': 10})]
        combatant_states = {c: CombatantState(c.name, c.hp_max, c.spell_slot_max) for c in combatants}
        state = CombatState(combatant_states)

        state.generate_children(combatants[0])
        best_action = state.choose_maximum_utility_child()
        expected = (player_attack_1, combatants[2])
        self.assertEqual(expected, best_action)

    def test_choose_highest_utility_child_when_no_possible_eliminations(self):
        damage_1 = [DamageData((1, D8), 1, 'bludgeoning')]
        player_attack_1 = WeaponAttack('Melee', 6, damage_1)
        damage_2 = [DamageData((1, D12), 2, 'slashing')]
        player_attack_2 = WeaponAttack('Melee', 4, damage_2)

        combatants = [
            PlayerCharacter({
                'name': 'p1',
                'HP_Max': 10,
                'Actions': {
                    'Weapon_Attacks': [player_attack_1, player_attack_2]}
            }),
            EnemyCharacter({'name': 'e1', 'HP_Max': 30, 'AC': 14}),
            EnemyCharacter({'name': 'e2', 'HP_Max': 25, 'AC': 10})]
        combatant_states = {c: CombatantState(c.name, c.hp_max, c.spell_slot_max) for c in combatants}
        state = CombatState(combatant_states)

        state.generate_children(combatants[0])
        best_action = state.choose_maximum_utility_child()
        expected = (player_attack_2, combatants[2])
        self.assertEqual(expected, best_action)


class TestExpectimax(TestCase):
    pass
