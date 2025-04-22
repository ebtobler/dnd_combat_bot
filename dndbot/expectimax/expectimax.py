from copy import copy

from dndbot.expectimax.combat_state import CombatState
from dndbot.characters.combatant import CombatantState, Combatant
from dndbot.characters.enemies.enemy_character import EnemyCharacter
from dndbot.characters.players.player_character import PlayerCharacter


class Expectimax:

    def __init__(self, players: list[PlayerCharacter], enemies: list[EnemyCharacter]):
        self.combatants = players + enemies
        initiatives = [(combatant.roll_initiative(), combatant) for combatant in self.combatants]
        initiatives.sort(reverse=True)
        self.turn_order = [combatant[1] for combatant in initiatives]
        initial_states = {c: CombatantState(c.name, c.hp_max, c.spell_slot_max) for c in self.combatants}
        self.root = CombatState(initial_states)
        self.current_state = self.root

    def expand_subtree(self, node: CombatState, turn: Combatant, depth: int):
        num_expanded = 0
        num_generated = 0
        current_layer = [node]
        next_layer = []
        current_turn_index = self.turn_order.index(turn)
        for c in range(current_turn_index, current_turn_index + depth):
            for state in current_layer:
                state.expand_children(self.turn_order[c % len(self.turn_order)])
                if state.children is not None:
                    for option in state.children:
                        successor_states = [prob_state_pair[1] for prob_state_pair in option[2]]
                        next_layer.extend(successor_states)
                    num_expanded += 1
            num_generated += len(next_layer)
            current_layer = copy(next_layer)
            next_layer.clear()
        return num_expanded, num_generated

    def play(self):
        pass
