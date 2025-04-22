from unittest import TestCase

from dndbot.expectimax.actions.damage_data import DamageData
from dndbot.dice.dice import D12, D6, D4
from dndbot.input_parsing.string_parser import StringParser


class TestStringParser(TestCase):

    def test_str_to_dice_function(self):
        dice_str = '2d6'
        result = StringParser.str_to_dice_function(dice_str)
        self.assertEqual(int, type(result[0]))
        self.assertEqual(2, result[0])
        self.assertEqual(D6, result[1])

    def test_parse_damage_string(self):
        dmg_string = '10d12 + 18 force damage, 8d4 + 12 fire damage'
        result = StringParser.parse_damage_string(dmg_string)
        expected_damage = DamageData((10, D12), 18, 'force')
        self.assertEqual(expected_damage, result)

    def test_parse_damage_string_takes_first_instance(self):
        dmg_string = '10d12 + 18 force damage, 8d4 + 12 fire damage'
        result = StringParser.parse_damage_string(dmg_string)
        expected_damage = DamageData((10, D12), 18, 'force')
        self.assertEqual(expected_damage, result)

    def test_parse_player_attack_string(self):
        attack_string = 'Melee Weapon Attack: +3 to hit, reach 5 ft. Hit: 2d6 + 3 slashing damage, 1d4 + 1 fire damage.'
        weapon_type, hit, damage = StringParser.parse_player_attack_string(attack_string)
        first_damage = DamageData((2, D6), 3, 'slashing')
        second_damage = DamageData((1, D4), 1, 'fire')
        expected_damage = [first_damage, second_damage]
        self.assertEqual('Melee', weapon_type)
        self.assertEqual(3, hit)
        self.assertEqual(expected_damage, damage)

    def test_parse_player_attack_string_with_no_reach_specified(self):
        attack_string = 'Melee Weapon Attack: +3 to hit. Hit: 2d6 + 3 slashing damage, 1d4 + 1 fire damage.'
        weapon_type, hit, damage = StringParser.parse_player_attack_string(attack_string)
        first_damage = DamageData((2, D6), 3, 'slashing')
        second_damage = DamageData((1, D4), 1, 'fire')
        expected_damage = [first_damage, second_damage]
        self.assertEqual('Melee', weapon_type)
        self.assertEqual(3, hit)
        self.assertEqual(expected_damage, damage)
