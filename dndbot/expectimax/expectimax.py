from copy import copy, deepcopy

from dndbot.expectimax.combat_state import CombatState
from dndbot.characters.combatant import CombatantState, Combatant
from dndbot.characters.enemies.enemy_character import EnemyCharacter
from dndbot.characters.players.player_character import PlayerCharacter


class Expectimax:

    def __init__(self, players: list[PlayerCharacter], enemies: list[EnemyCharacter]):
        self.combatants = []
        for c in players + enemies:
            if c in self.combatants:
                c_copy = deepcopy(c)
                n = 1
                appended = False
                while not appended:
                    if c_copy in self.combatants:
                        n += 1
                        c_copy.name = c.name + f'_{n}'
                    else:
                        self.combatants.append(c_copy)
                        appended = True
            else:
                self.combatants.append(c)

        initiatives = [(combatant.roll_initiative(), combatant) for combatant in self.combatants]
        initiatives.sort(reverse=True)
        self.turn_order = [combatant[1] for combatant in initiatives]
        initial_states = {c: CombatantState(c.name, c.hp_max, c.spell_slot_max) for c in self.combatants}
        self.root = CombatState(initial_states)
        self.current_state = self.root
        self.combat_log = []
        self.outcome = 'none'

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

    def make_move(self, turn: Combatant, verbose: bool = True):
        if self.current_state.children is None:
            return 'terminal'
        elif turn.team == 'player':
            (action, target) = self.current_state.choose_maximum_utility_child()
        else:
            (action, target) = self.current_state.choose_minimum_utility_child()
        self.combat_log.append((self.current_state, turn, action, target))
        if verbose:
            print(self.current_state)
            print(turn, 'taking action', action, 'against', target)
        self.current_state = action.perform(target, self.current_state, verbose=verbose)

        combatants_alive = set(filter(lambda x: x != 0,
                                      [c[0] if c[1].hp > 0 else 0 for c in
                                       self.current_state.combatant_states.items()]))
        for c in self.turn_order:
            if c not in combatants_alive:
                self.turn_order.remove(c)

        if verbose:
            print()

        next_turn_idx = self.turn_order.index(turn) + 1
        if next_turn_idx >= len(self.turn_order):
            next_turn_idx = 0
        return next_turn_idx

    def play(self, verbose: bool = True):
        turn_index = 0
        expanded = 0
        generated = 0
        turns_taken = 0
        rounds = 0
        while self.current_state.outcome == 0:
            turn = self.turn_order[turn_index]
            ex, gen = self.expand_subtree(self.current_state, turn, 3)
            expanded += ex
            generated += gen
            turn_index = self.make_move(turn, verbose=verbose)
            turns_taken += 1
            if turn_index == 0:
                rounds += 1

        if verbose:
            print(self.current_state)
            if self.current_state.outcome == 1:
                print('Players win!')
            elif self.current_state.outcome == -1:
                print('Enemies win!')
            else:
                print('uh oh')

        return turns_taken - 1, rounds, expanded, generated
