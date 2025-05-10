import time

from dndbot.characters.enemies.enemy_character import EnemyCharacter
from dndbot.characters.players.player_character import PlayerCharacter
from dndbot.expectimax.expectimax import Expectimax
from run_cases.setup_helpers import SetupHelpers
from stats.stats_helpers import StatsHelpers


class RunCases:
    @staticmethod
    def run():
        RunCases.default()

    @staticmethod
    def default():
        players = SetupHelpers.get_player_characters_from_user()
        enemies = SetupHelpers.get_enemy_characters_from_user()

        if len(players) == 0 and len(enemies) == 0:
            print("No players or enemies!")
            return
        elif len(players) == 0:
            print("No players!")
            return
        elif len(enemies) == 0:
            print("No enemies!")
            return

        num_trials = -1
        while num_trials < 1:
            num_trials = int(input('Number of simulations to run (integer greater than 0): '))

        if num_trials == 1:
            expectimax = Expectimax(players, enemies)
            turns_taken, rounds, expanded, generated = expectimax.play()
            print(f'{turns_taken} turns taken, {rounds} rounds played')
            print(f'{expanded} nodes expanded, {generated} nodes generated')
        else:
            RunCases.average_outcome(players, enemies, num_trials)

    @staticmethod
    def average_outcome(players: list[PlayerCharacter], enemies: list[EnemyCharacter], trials: int):
        print('Players: ', end='')
        print(players)
        print('Enemies: ', end='')
        print(enemies)
        print('Trials:', trials)

        avg_turns, avg_expanded, avg_generated, avg_time, player_winrate = \
            AverageOutcomeStats.run(players, enemies, trials)

        print(f'avg turns:           {avg_turns}')
        print(f'avg nodes expanded:  {avg_expanded}')
        print(f'avg nodes generated: {avg_generated}')
        print(f'avg run time:        {avg_time} s')
        print(f'player winrate:      {player_winrate * 100}%')
        print()

    @staticmethod
    def average_performance(trials: int):
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
        two_two = ([jorge, anduil], [goblin, goblin])
        two_three = ([jorge, anduil], [goblin, goblin, goblin])
        two_four = ([jorge, anduil], [goblin, goblin, goblin, goblin])
        four_four = ([jorge, jorge, anduil, anduil], [goblin, goblin, goblin, goblin])
        return [one_one, one_two, two_two, two_three, two_four, four_four]

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
