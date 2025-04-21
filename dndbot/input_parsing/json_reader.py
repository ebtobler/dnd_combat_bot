from json import loads

from dndbot.battle.expectimax.actions.weapon_attack import WeaponAttack
from dndbot.characters.enemies.enemy_character import EnemyCharacter
from dndbot.characters.players.player_character import PlayerCharacter
from dndbot.input_parsing.string_parser import StringParser


class JsonReader:

    @staticmethod
    def parse_player_character(file: str) -> PlayerCharacter:
        with open(file, 'r') as file:
            f_str = file.read()
        char_stats = loads(f_str)
        weapon_attacks = char_stats['Actions']['Weapon_Attacks']
        char_stats['Actions']['Weapon_Attacks'] = [
            WeaponAttack(*StringParser.parse_player_attack_string(a))
            for a
            in weapon_attacks]
        return PlayerCharacter(char_stats)

    @staticmethod
    def parse_enemy_character(file: str) -> EnemyCharacter:
        with open(file, 'r') as file:
            f_str = file.read()
        char_stats = loads(f_str)
        return EnemyCharacter(char_stats)
