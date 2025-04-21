from unittest import TestCase
from unittest.mock import patch

from dndbot.battle.battle import Battle
from dndbot.characters.enemies.enemy_character import EnemyCharacter
from dndbot.characters.players.player_character import PlayerCharacter
from dndbot.dice.dice import Dice, D20


class TestBattle(TestCase):

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
        b = Battle(players, enemies)
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
        b = Battle(players, enemies)
        expected_order = [players[0], players[1], enemies[0], enemies[1]]
        self.assertEqual(b.turn_order, expected_order)

