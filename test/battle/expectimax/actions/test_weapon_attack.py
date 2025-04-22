from unittest import TestCase

from dndbot.battle.expectimax.actions.damage_data import DamageData
from dndbot.battle.expectimax.actions.weapon_attack import WeaponAttack
from dndbot.characters.enemies.enemy_character import EnemyCharacter
from dndbot.dice.dice import D6, D4


class TestWeaponAttack(TestCase):

    def test_hit_chance(self):
        attack = WeaponAttack('untyped', 4, [])
        target = EnemyCharacter({'AC': 14})
        result = attack.hit_chance(target)
        self.assertEqual(.5, result)

    def test_average_damage(self):
        damage = [DamageData((1, D6), 1, 'untyped'), DamageData((2, D4), 1, 'force')]
        attack = WeaponAttack('untyped', 0, damage)
        result = attack.average_damage()
        expected = 3.5 + 1 + 2.5 * 2 + 1
        self.assertEqual(10.5, result)
