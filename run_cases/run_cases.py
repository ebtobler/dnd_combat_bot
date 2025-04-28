import time
from os import path

from dndbot.expectimax.expectimax import Expectimax
from dndbot.input_parsing.json_reader import JsonReader
from stats.stats_helpers import StatsHelpers


class RunCases:
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


class AverageOutcomeStats:

    @staticmethod
    def run(players, enemies, trials: int):
        sum_turns = 0
        sum_expanded = 0
        sum_generated = 0
        sum_time = 0

        for t in range(trials):
            expectimax = Expectimax(players, enemies)
            start_time = time.perf_counter()
            turns_taken, _, expanded, generated = expectimax.play(verbose=False)
            end_time = time.perf_counter()

            sum_turns += turns_taken
            sum_expanded += expanded
            sum_generated += generated
            sum_time += end_time - start_time

        avg_turns = sum_turns / trials
        avg_expanded = sum_expanded / trials
        avg_generated = sum_generated / trials
        avg_time = sum_time / trials
        return avg_turns, avg_expanded, avg_generated, avg_time
