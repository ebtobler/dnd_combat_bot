from dataclasses import dataclass

from dndbot.expectimax.action import Action
from dndbot.characters.combatant import CombatantState, Combatant


@dataclass
class CombatState:

    # children member is list of tuples of (action, target, outcome_states)
    # outcome_states is list of tuples of (probability, state)
    combatant_states: dict[Combatant: CombatantState]
    children: list[tuple[Action, Combatant, list[tuple[float, "CombatState"]]]] or None
    player_w = 5
    enemy_w = 3

    def __init__(self, combatant_states: dict[Combatant: CombatantState]):
        self.combatant_states = combatant_states
        self.children = None

    """
    There are a few different utility functions I've come up with:
    u1 = total_player_health - total_enemy_health
    u2 = total_player_health + w * players_alive - total_enemy_health - w * enemies_alive
    u3 = damage_dealt_by_players - damage_dealt_by_enemies
    u4 = damage_dealt_by_players + w * players_alive - damage_dealt_by_enemies - w * enemies_alive
    u5 = total_player_health / total_enemy_health 
    damage and health might be equivalent
    """
    def utility(self, probability: float = None):
        u = self.weighted_health_utility()
        if probability is None:
            return u
        return probability * u

    def health_utility(self):
        return sum([c[1].hp if c[0].team == 'player' else -1 * c[1].hp for c in self.combatant_states.items()])

    def weighted_health_utility(self):
        players = list(filter(lambda x: x > 0,
                              [c[1].hp if c[0].team == 'player' else 0 for c in self.combatant_states.items()]))
        player_health = sum(players)
        player_health += self.player_w * len(players)
        enemies = list(filter(lambda x: x > 0,
                              [c[1].hp if c[0].team == 'enemy' else 0 for c in self.combatant_states.items()]))
        enemy_health = sum(enemies)
        enemy_health += self.enemy_w * len(enemies)
        return player_health - enemy_health

    # doesn't seem as good as health utility
    def weighted_proportion_utility(self):
        players = list(filter(lambda x: x > 0,
                              [c[1].hp if c[0].team == 'player' else 0 for c in self.combatant_states.items()]))
        player_health = sum(players)
        player_health += self.player_w * len(players)
        enemies = list(filter(lambda x: x > 0,
                              [c[1].hp if c[0].team == 'enemy' else 0 for c in self.combatant_states.items()]))
        enemy_health = sum(enemies)
        enemy_health += self.enemy_w * len(enemies)
        return player_health / enemy_health

    def choose_maximum_utility_child(self):
        maximum_utility_action = None
        maximum_utility = float('-inf')
        for action in self.children:
            action_utility = sum([child_state[1].utility(probability=child_state[0]) for child_state in action[2]])
            if action_utility > maximum_utility:
                maximum_utility = action_utility
                maximum_utility_action = (action[0], action[1])
        return maximum_utility_action

    def choose_minimum_utility_child(self):
        minimum_utility_action = None
        minimum_utility = float('-inf')
        for action in self.children:
            action_utility = sum([child_state[1].utility(child_state[0]) for child_state in action[2]])
            if action_utility > minimum_utility:
                minimum_utility = action_utility
                minimum_utility_action = (action[0], action[1])
        return minimum_utility_action

    def expand_children(self, current_turn: Combatant):
        if self.children is not None:
            return
        children = []
        actions = current_turn.actions
        for action_type in actions.values():
            for action in action_type:
                targets = list(filter(lambda x: x.team != current_turn.team,
                                      [c for c in self.combatant_states.keys()]))
                for t in targets:
                    children.append(action.generate_states(self, t))
        self.children = children
