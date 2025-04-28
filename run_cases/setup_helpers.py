from os import path

from dndbot.input_parsing.json_reader import JsonReader
from stats.stats_helpers import StatsHelpers


class SetupHelpers:
    @staticmethod
    def jorge():
        jorge = JsonReader.parse_player_character(
            path.join(StatsHelpers.stats_folder_path(), 'players', 'jorge.json')
        )
        return jorge

    @staticmethod
    def anduil():
        anduil = JsonReader.parse_player_character(
            path.join(StatsHelpers.stats_folder_path(), 'players', 'anduil.json')
        )
        return anduil

    @staticmethod
    def goblin():
        goblin = JsonReader.parse_enemy_character(
            path.join(StatsHelpers.stats_folder_path(), 'enemies', 'goblin.json')
        )
        return goblin

    @staticmethod
    def barbarian():
        barb = JsonReader.parse_player_character(
            path.join(StatsHelpers.stats_folder_path(), 'players', 'barbarian.json')
        )
        return barb
