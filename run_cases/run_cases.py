import time

from dndbot.expectimax.expectimax import Expectimax
from run_cases.setup_helpers import SetupHelpers

class RunCases:
    @staticmethod
    def run():
        # RunCases.default()
        RunCases.average_outcome(20)

    @staticmethod
    def default():
        players = [SetupHelpers.jorge()]
        enemies = [SetupHelpers.goblin(), SetupHelpers.goblin()]

        if len(players) == 0 and len(enemies) == 0:
            print("No players or enemies!")
        elif len(players) == 0:
            print("No players!")
        elif len(enemies) == 0:
            print("No enemies!")

        expectimax = Expectimax(players, enemies)
        turns_taken, rounds, expanded, generated = expectimax.play()
        print(f'{turns_taken} turns taken, {rounds} rounds played')
        print(f'{expanded} nodes expanded, {generated} nodes generated')

    @staticmethod
    def average_outcome(trials: int):
        cases = AverageOutcomeStats.combat_cases_incremental()[0:-1]
        for case in cases:
            players = case[0]
            enemies = case[1]
            print(f'statistics for {len(players)} players and {len(enemies)} enemies over {trials} trials:')

            avg_turns, avg_expanded, avg_generated, avg_time, player_winrate = \
                AverageOutcomeStats.run(players, enemies, trials)

            print(f'avg turns:           {avg_turns}')
            print(f'avg nodes expanded:  {avg_expanded}')
            print(f'avg nodes generated: {avg_generated}')
            print(f'avg run time:        {avg_time}')
            print(f'player winrate:      {player_winrate * 100}%')
            print()
        print("Done")


class AverageOutcomeStats:

    @staticmethod
    def combat_cases_incremental():
        jorge = SetupHelpers.jorge()
        anduil = SetupHelpers.anduil()
        goblin = SetupHelpers.goblin()
        one_one = ([jorge], [goblin])
        one_two = ([jorge], [goblin, goblin])
        two_four = ([jorge, anduil], [goblin, goblin, goblin, goblin])
        four_four = ([jorge, jorge, anduil, anduil], [goblin, goblin, goblin, goblin])
        return [one_one, one_two, two_four, four_four]

    @staticmethod
    def run(players, enemies, trials: int):
        sum_turns = 0
        sum_expanded = 0
        sum_generated = 0
        sum_time = 0
        player_wins = 0
        enemy_wins = 0

        for t in range(trials):
            expectimax = Expectimax(players, enemies)
            start_time = time.perf_counter()
            turns_taken, _, expanded, generated = expectimax.play(verbose=False)
            end_time = time.perf_counter()
            if expectimax.current_state.outcome == 1:
                player_wins += 1
            elif expectimax.current_state.outcome == -1:
                enemy_wins += 1
            else:
                print(f"unexpected outcome: {expectimax.outcome}")
                exit(-1)

            sum_turns += turns_taken
            sum_expanded += expanded
            sum_generated += generated
            sum_time += end_time - start_time

        avg_turns = sum_turns / trials
        avg_expanded = sum_expanded / trials
        avg_generated = sum_generated / trials
        avg_time = sum_time / trials
        player_winrate = player_wins / trials
        return avg_turns, avg_expanded, avg_generated, avg_time, player_winrate
