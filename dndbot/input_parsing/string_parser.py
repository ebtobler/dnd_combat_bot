from re import search

from dndbot.battle.expectimax.actions.damage_data import DamageData
from dndbot.dice.dice import Dice


class StringParser:
    """
    takes in a string in format '[n]d[s]' where
    n is the number of dice and s is the number of sides on the dice

    returns a pair of (n, roll_function)
    """
    @staticmethod
    def str_to_dice_function(dice_str: str):
        n_str = search(r'\d+', dice_str).group()
        die = dice_str.split(n_str)[1]
        n = int(n_str)

        if die == 'd100':
            roll_function = Dice.d100
        elif die == 'd20':
            roll_function = Dice.d20
        elif die == 'd12':
            roll_function = Dice.d12
        elif die == 'd10':
            roll_function = Dice.d10
        elif die == 'd8':
            roll_function = Dice.d8
        elif die == 'd6':
            roll_function = Dice.d6
        elif die == 'd4':
            roll_function = Dice.d4
        else:
            roll_function = Dice.d1

        return n, roll_function

    """
    format is:
    [Melee / Ranged] Weapon Attack: +[x] to hit, reach [r] ft. Hit: [n]d[s] + [m] [type] damage, [n]d[s] + [m] [type] damage, ...
    """
    @staticmethod
    def parse_player_attack_string(attack_str: str):
        components = attack_str.split(': ')
        weapon_type = components[0].split(' ')[0]
        hit_mod = int(components[1].split(' ')[0])
        damage_str = components[2]
        damage_instances_str = damage_str.split(', ')
        damage_instances = []
        for dmg in damage_instances_str:
            damage_instances.append(StringParser.parse_damage_string(dmg))
        return weapon_type, hit_mod, damage_instances

    """
    damage string should be formatted as: [n]d[s] + [x] [type], [n]d[s] + [x] [type], ...
    e.g.: 2d6 + 3 slashing, 2d4 + 1 force
    """
    @staticmethod
    def parse_damage_string(dmg: str):
        components = dmg.split(' ')
        damage_dice = StringParser.str_to_dice_function(components[0])
        modifier = int(components[2]) if components[1] == '+' else -1 * int(components[2])
        return DamageData(damage_dice, modifier, components[3])
