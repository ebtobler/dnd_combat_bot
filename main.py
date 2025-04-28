from os import path

from dndbot.expectimax.expectimax import Expectimax
from dndbot.input_parsing.json_reader import JsonReader
from stats.stats_helpers import StatsHelpers

if __name__ == '__main__':
    jorge = JsonReader.parse_player_character(
        path.join(StatsHelpers.stats_folder_path(), 'players', 'jorge.json'))
    players = [jorge]
    goblin = JsonReader.parse_enemy_character(
        path.join(StatsHelpers.stats_folder_path(), 'enemies', 'goblin.json'))
    enemies = [goblin, goblin]
    if len(players) == 0 and len(enemies) == 0:
        print("No players or enemies!")
    elif len(players) == 0:
        print("No players!")
    elif len(enemies) == 0:
        print("No enemies!")
    expectimax = Expectimax(players, enemies)
    expectimax.play()
