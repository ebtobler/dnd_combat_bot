from dataclasses import dataclass

from dndbot.battle.battle import Battle
from dndbot.battle.expectimax.action import Action
from dndbot.characters.combatant import CombatantState, Combatant


@dataclass
class CombatState:

    children: list[tuple[Action, list[tuple[float, "CombatState"]]]] or None

    def __init__(self, combatant_states: dict[Combatant: CombatantState]):
        self.combatant_states = combatant_states
        self.children = None

    """
    There are a few different utility functions I've come up with:
    u1 = total_player_health - total_enemy_health
    u2 = total_player_health + w * players_alive - total_enemy_health - w * enemies_alive
    u3 = damage_dealt_by_players - damage_dealt_by_enemies
    u4 = damage_dealt_by_players + w * players_alive - damage_dealt_by_enemies - w * enemies_alive
    damage and health might be equivalent
    """
    def utility(self, probability: float = None):
        u = sum([c[1].hp if c[0].team == 'player' else -1 * c[1].hp for c in self.combatant_states.items()])
        if probability is None:
            return u
        return probability * u

    def choose_highest_utility_child(self):
        highest_utility_action = None
        highest_utility = float('-inf')
        for action in self.children:
            action_utility = sum([child_state[1].utility(child_state[0]) for child_state in action[1]])
            if action_utility > highest_utility:
                highest_utility = action_utility
                highest_utility_action = action[0]
        return highest_utility_action

    def generate_children(self, current_turn: Combatant):
        if self.children is not None:
            return

        children = []
        actions = current_turn.actions
        for action_type in actions:
            for action in action_type:
                children.append()


class Expectimax:

    def __init__(self, battle: Battle):
        self.battle = battle
        initial_states = [CombatantState(c['name'], c['HP'], c['Spell_Slots']) for c in battle.combatants]
        self.root = CombatState(initial_states)

    def generate_subtree(self, depth: int):
        pass

    def play(self):
        pass
