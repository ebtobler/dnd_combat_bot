from unittest import TestCase

from dndbot.expectimax.actions.damage_data import DamageData
from dndbot.dice.dice import D6, D10


class TestDamageData(TestCase):

    def test_avg_damage_with_one_die(self):
        dmg = DamageData((1, D6), 1, 'untyped')
        self.assertEqual(4.5, dmg.average_damage())

    def test_avg_damage_with_multiple_dice(self):
        dmg = DamageData((3, D10), 3, 'untyped')
        self.assertEqual(19.5, dmg.average_damage())
