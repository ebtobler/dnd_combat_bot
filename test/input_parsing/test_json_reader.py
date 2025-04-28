from os import path
from unittest import TestCase

from dndbot.expectimax.actions.damage_data import DamageData
from dndbot.expectimax.actions.weapon_attack import WeaponAttack
from dndbot.dice.dice import D6, D4
from dndbot.input_parsing.json_reader import JsonReader


class TestJsonReader(TestCase):

    def test_parse_player_character(self):
        jorge_file = path.join(path.dirname(__file__), '..', '..', 'stats', 'players', 'jorge.json')
        jorge = JsonReader.parse_player_character(jorge_file)
        expected_ability_scores = {
            "STR": 16, "STR_mod": 3,
            "DEX": 14, "DEX_mod": 2,
            "CON": 16, "CON_mod": 3,
            "INT": 9, "INT_mod": -1,
            "WIS": 12, "WIS_mod": 1,
            "CHA": 10, "CHA_mod": 0
        }
        expected_saving_throws = {"STR": 5, "DEX": 2, "CON": 5, "INT": -1, "WIS": 1, "CHA": 0}
        expected_actions = {
            "Weapon_Attacks": [
                WeaponAttack('Melee', 3, tuple([DamageData((1, D6), 3, 'slashing')])),
                WeaponAttack('Melee', 5, tuple([DamageData((1, D4), 3, 'bludgeoning')])),
                WeaponAttack('Ranged', 3, tuple([DamageData((1, D6), 1, 'piercing')])),
            ]
        }
        expected_spells = {
            '0': ['Fire Bolt'],
            '1': [],
            '2': [],
            '3': [],
            '4': [],
            '5': [],
            '6': [],
            '7': [],
            '8': [],
            '9': [],
        }
        self.assertEqual('Jorge', jorge.name)
        self.assertEqual(17, jorge.ac)
        self.assertEqual(24, jorge.hp_max)
        self.assertEqual(2, jorge.initiative)
        self.assertEqual(30, jorge.speed)
        self.assertEqual(expected_ability_scores, jorge.ability_scores)
        self.assertEqual(expected_saving_throws, jorge.saving_throws)
        self.assertEqual(expected_actions, jorge.actions)
        self.assertEqual(expected_spells, jorge.spells)
