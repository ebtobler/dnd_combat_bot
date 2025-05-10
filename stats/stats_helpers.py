from os import path, listdir


class StatsHelpers:

    @staticmethod
    def stats_folder_path():
        return path.dirname(__file__)

    @staticmethod
    def display_available_players():
        players_directory = path.join(StatsHelpers.stats_folder_path(), 'players')
        print('Players:')
        for file in listdir(players_directory):
            print(file)
        print()

    @staticmethod
    def display_available_enemies():
        enemies_directory = path.join(StatsHelpers.stats_folder_path(), 'enemies')
        print('Enemies:')
        for file in listdir(enemies_directory):
            print(file)
        print()
