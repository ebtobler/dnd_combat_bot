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
        self.combat_log = []

    def expand_subtree(self, node: CombatState, turn: Combatant, depth: int):
        num_expanded = 0
        num_generated = 0
        current_layer = [node]
        next_layer = []
        current_turn_index = self.turn_order.index(turn)
        for c in range(current_turn_index, current_turn_index + depth):
            for state in current_layer:
                if state.children is None:
                    state.expand_children(self.turn_order[c % len(self.turn_order)])
                    if state.children is not None:
                        num_expanded += 1
                        num_generated += len([s for states in list(state.children.values()) for s in states])
                        if current_turn_index != current_turn_index + depth - 1:
                            for (action, states) in state.children.items():
                                successor_states = [prob_state_pair[1] for prob_state_pair in states]
                                next_layer.extend(successor_states)
                elif current_turn_index != current_turn_index + depth - 1:
                    for (action, states) in state.children.items():
                        successor_states = [prob_state_pair[1] for prob_state_pair in states]
                        next_layer.extend(successor_states)
            current_layer = copy(next_layer)
            next_layer.clear()
        return num_expanded, num_generated

    def make_move(self, turn: Combatant):
        if self.current_state.children is None:
            return 'terminal'
        elif turn.team == 'player':
            (action, target) = self.current_state.choose_maximum_utility_child()
        else:
            (action, target) = self.current_state.choose_minimum_utility_child()
        self.combat_log.append((self.current_state, turn, action, target))
        print(self.current_state)
        print(turn, 'taking action', action, 'against', target)
        self.current_state = action.perform(target, self.current_state)

        combatants_alive = set(filter(lambda x: x != 0,
                                      [c[0] if c[1].hp > 0 else 0 for c in
                                       self.current_state.combatant_states.items()]))
        for c in self.turn_order:
            if c not in combatants_alive:
                self.turn_order.remove(c)

        print()

    def play(self):
        turn_index = 0
        while self.current_state.outcome == 0:
            turn = self.turn_order[turn_index]
            self.expand_subtree(self.current_state, turn, 3)
            self.make_move(turn)
            turn_index = (turn_index + 1) % len(self.turn_order)

        print(self.current_state)
        if self.current_state.outcome == 1:
            print('Players win!')
        elif self.current_state.outcome == -1:
            print('Enemies win!')
        else:
            print('uh oh')
