from dndbot.expectimax.expectimax import Expectimax
from test._dnd_utils.dnd_utils import DndUtils

if __name__ == '__main__':
    players, enemies = DndUtils.two_players_two_enemies_two_attacks()
    expectimax = Expectimax(players, enemies)
    expectimax.play()
