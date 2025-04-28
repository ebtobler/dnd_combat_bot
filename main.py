from dndbot.expectimax.expectimax import Expectimax
from run_cases.run_cases import RunCases

if __name__ == '__main__':
    players = [RunCases.jorge()]
    enemies = [RunCases.goblin(), RunCases.goblin()]

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

