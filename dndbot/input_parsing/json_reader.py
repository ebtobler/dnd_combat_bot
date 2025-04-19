from json import loads

from dndbot.characters.enemies.enemy_character import EnemyCharacter
from dndbot.characters.players.player_character import PlayerCharacter


class JsonReader:

    @staticmethod
    def parse_player_character(file: str) -> PlayerCharacter:
        with open(file, 'r') as file:
            f_str = file.read()
        char_stats = loads(f_str)
        return PlayerCharacter(char_stats)

    @staticmethod
    def parse_enemy_character(file: str) -> EnemyCharacter:
        with open(file, 'r') as file:
            f_str = file.read()
        char_stats = loads(f_str)
        return EnemyCharacter(char_stats)
