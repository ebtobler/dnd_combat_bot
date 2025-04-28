from os import path
from unittest import TestCase

from dndbot.dice.dice import D6
from dndbot.expectimax.actions.damage_data import DamageData
from dndbot.expectimax.actions.weapon_attack import WeaponAttack
from dndbot.input_parsing.json_reader import JsonReader
from stats.stats_helpers import StatsHelpers


class TestReadEnemyJson(TestCase):

    def test_goblin_json(self):
        goblin_file = path.join(StatsHelpers.stats_folder_path(), 'enemies', 'goblin.json')
        goblin = JsonReader.parse_enemy_character(goblin_file)

        scimitar_damage = tuple([DamageData((1, D6), 2, 'slashing')])
        scimitar = WeaponAttack('Melee', 4, scimitar_damage)
        shortbow_damage = tuple([DamageData((1, D6), 2, 'piercing')])
        shortbow = WeaponAttack('Ranged', 4, shortbow_damage)

        expected_weapon_attacks = [scimitar, shortbow]

        expected = {
            'name': 'Goblin',
            'ac': 15,
            'hp': 7,
            'speed': 30,
            'ability_scores': {
                'STR': 8, 'STR_mod': -1,
                'DEX': 14, 'DEX_mod': 2,
                'CON': 10, 'CON_mod': 0,
                'INT': 10, 'INT_mod': 0,
                'WIS': 8, 'WIS_mod': -1,
                'CHA': 8, 'CHA_mod': -1
            },
            'actions': {
                'Weapon_Attacks': expected_weapon_attacks
            }
        }

        self.assertEqual(expected['name'], goblin.name)
        self.assertEqual(expected['ac'], goblin.ac)
        self.assertEqual(expected['hp'], goblin.hp_max)
        self.assertEqual(expected['speed'], goblin.speed)
        self.assertEqual(expected['ability_scores'], goblin.ability_scores)
        self.assertEqual(expected['actions'], goblin.actions)
