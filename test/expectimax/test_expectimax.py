from unittest import TestCase
from unittest.mock import patch

from dndbot.expectimax.actions.damage_data import DamageData
from dndbot.expectimax.actions.weapon_attack import WeaponAttack
from dndbot.expectimax.expectimax import Expectimax
from dndbot.characters.enemies.enemy_character import EnemyCharacter
from dndbot.characters.players.player_character import PlayerCharacter
from dndbot.dice.dice import D20, D12, D6
from test._dnd_utils.dnd_utils import DndUtils


class TestExpectimax(TestCase):

    @patch.object(D20, 'roll')
    def test_initiative_ordered_correctly(self, mock_d20):
        mock_d20.side_effect = [[1], [2], [3], [4]]
        players = [
            PlayerCharacter({'name': 'player1', 'Initiative': 0}),
            PlayerCharacter({'name': 'player2', 'Initiative': 0}),
        ]
        enemies = [
            EnemyCharacter({'name': 'enemy1', 'Initiative': 0}),
            EnemyCharacter({'name': 'enemy2', 'Initiative': 0}),
        ]
        b = Expectimax(players, enemies)
        expected_order = [enemies[1], enemies[0], players[1], players[0]]
        self.assertEqual(b.turn_order, expected_order)

    @patch.object(D20, 'roll', return_value=[10])
    def test_initiative_bonuses_taken_into_account(self, mock_d20):
        players = [
            PlayerCharacter({'name': 'player1', 'Initiative': 4}),
            PlayerCharacter({'name': 'player2', 'Initiative': 3}),
        ]
        enemies = [
            EnemyCharacter({'name': 'enemy1', 'Initiative': 2}),
            EnemyCharacter({'name': 'enemy2', 'Initiative': 1}),
        ]
        b = Expectimax(players, enemies)
        expected_order = [players[0], players[1], enemies[0], enemies[1]]
        self.assertEqual(b.turn_order, expected_order)

    @patch.object(D20, 'roll', return_value=[10])
    def test_initiative_with_equal_rolls(self, mock_d20):
        players = [
            PlayerCharacter({'name': 'player1', 'Initiative': 1, 'Ability_Scores': {'DEX': 3}}),
            PlayerCharacter({'name': 'player2', 'Initiative': 1, 'Ability_Scores': {'DEX': 2}}),
        ]
        enemies = [
            EnemyCharacter({'name': 'enemy1', 'Initiative': 1, 'Ability_Scores': {'DEX': 1}}),
            EnemyCharacter({'name': 'enemy2', 'Initiative': 1, 'Ability_Scores': {'DEX': 0}}),
        ]
        b = Expectimax(players, enemies)
        expected_order = [players[0], players[1], enemies[0], enemies[1]]
        self.assertEqual(b.turn_order, expected_order)

    def test_expand_subtree_does_not_generate_children_for_terminal_nodes(self):
        player, enemy = DndUtils.single_player_and_enemy()
        enemy[0].hp_max = 3
        exp = Expectimax(player, enemy)
        num_expanded, num_generated = exp.expand_subtree(exp.root, player[0], 2)
        self.assertEqual(3, num_expanded)
        self.assertEqual(12, num_generated)

    def test_expand_subtree_with_nonterminal_leaves(self):
        players, enemies = DndUtils.two_players_two_enemies_two_attacks()
        exp = Expectimax(players, enemies)
        num_expanded, num_generated = exp.expand_subtree(exp.root, players[0], 2)

        expected_expanded = 1 + 2 * 2 * 2  # branching factor = 2 actions * 2 targets * 2 outcomes
        expected_generated = expected_expanded * 2 * 2 * 2
        self.assertEqual(expected_expanded, num_expanded)
        self.assertEqual(expected_generated, num_generated)

    def test_choose_max_child_with_subtree(self):
        player, enemy = DndUtils.single_player_and_enemy()
        exp = Expectimax(player, enemy)
        exp.expand_subtree(exp.root, player[0], 3)

        max_action = exp.root.choose_maximum_utility_child()
        expected = (WeaponAttack('Melee', 4, tuple([DamageData((1, D12), 1, 'bludgeoning')])), enemy[0])
        self.assertEqual(expected, max_action)

    def test_choose_min_child_with_subtree(self):
        player, enemy = DndUtils.single_player_and_enemy()
        exp = Expectimax(player, enemy)
        exp.expand_subtree(exp.root, enemy[0], 3)

        min_action = exp.root.choose_minimum_utility_child()

        expected = (WeaponAttack('Melee', 4, tuple([DamageData((1, D6), 3, 'slashing')])), player[0])
        self.assertEqual(expected, min_action)

    def test_make_move(self):
        player, enemy = DndUtils.single_player_and_enemy()
        exp = Expectimax(player, enemy)
        exp.expand_subtree(exp.root, player[0], 3)

        exp.make_move(player[0])
