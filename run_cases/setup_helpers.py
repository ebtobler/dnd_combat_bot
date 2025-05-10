from os import path

from dndbot.input_parsing.json_reader import JsonReader
from stats.stats_helpers import StatsHelpers


class SetupHelpers:

    @staticmethod
    def get_player_characters_from_user():
        user_input = 'init'
        players = []
        print("Creating players list, press 'Enter' to exit")
        while user_input != '':
            StatsHelpers.display_available_players()
            print("Current players: ", end='')
            print(players)
            user_input = input('Type player file name: ')
            if user_input != '':
                try:
                    p = JsonReader.parse_player_character(
                        path.join(StatsHelpers.stats_folder_path(), 'players', user_input)
                    )
                    players.append(p)
                except FileNotFoundError:
                    print("File not found, try again")
            print()
        return players

    @staticmethod
    def get_enemy_characters_from_user():
        user_input = 'init'
        enemies = []
        print("Creating enemies list, press 'Enter' to exit")
        while user_input != '':
            StatsHelpers.display_available_enemies()
            print("Current enemies: ", end='')
            print(enemies)
            user_input = input('Type enemy file name: ')
            if user_input != '':
                try:
                    e = JsonReader.parse_enemy_character(
                        path.join(StatsHelpers.stats_folder_path(), 'enemies', user_input)
                    )
                    enemies.append(e)
                except FileNotFoundError:
                    print("File not found, try again")
            print()
        return enemies

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
