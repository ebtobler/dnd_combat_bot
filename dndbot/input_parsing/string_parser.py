from re import search

from dndbot.expectimax.actions.damage_data import DamageData
from dndbot.dice.dice import D100, D20, D12, D10, D8, D6, D4, D1


class StringParser:
    """
    takes in a string in format '[n]d[s]' where
    n is the number of dice and s is the number of sides on the dice

    returns a pair of (n, roll_function)
    """
    @staticmethod
    def str_to_dice_function(dice_str: str):
        n_str, die = dice_str.split('d')
        die = 'd' + die
        n = int(n_str)

        if die == 'd100':
            dice_to_roll = D100
        elif die == 'd20':
            dice_to_roll = D20
        elif die == 'd12':
            dice_to_roll = D12
        elif die == 'd10':
            dice_to_roll = D10
        elif die == 'd8':
            dice_to_roll = D8
        elif die == 'd6':
            dice_to_roll = D6
        elif die == 'd4':
            dice_to_roll = D4
        else:
            dice_to_roll = D1

        return n, dice_to_roll

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
        damage_instances = tuple(damage_instances)
        return weapon_type, hit_mod, damage_instances

    """
    damage string should be formatted as: [n]d[s] + [x] [type], [n]d[s] + [x] [type], ...
    e.g.: 2d6 + 3 slashing, 2d4 + 1 force
    """
    @staticmethod
    def parse_damage_string(dmg: str):
        components = dmg.split(' ')
        damage_dice = tuple(StringParser.str_to_dice_function(components[0]))
        modifier = int(components[2]) if components[1] == '+' else -1 * int(components[2])
        return DamageData(damage_dice, modifier, components[3])
