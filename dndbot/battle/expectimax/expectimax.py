from dndbot.battle.battle import Battle
from dndbot.battle.expectimax.action import Action
from dndbot.characters.combatant import CombatantState, Combatant


class CombatState:

    children: list[tuple[Action, list[tuple[float, "CombatState"]]]]

    def __init__(self, combatant_states: dict[Combatant: CombatantState]):
        self.combatant_states = combatant_states

    def utility(self, probability: float):
        return probability * sum([c[1].hp if c[0].team == 'player' else -1 * c[1].hp for c in list(self.combatant_states)])

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
        pass


class Expectimax:

    def __init__(self, battle: Battle):
        self.battle = battle
        initial_states = [CombatantState(c['name'], c['HP'], c['Spell_Slots']) for c in battle.combatants]
        self.root = CombatState(initial_states)

    def generate_subtree(self, depth: int):
        pass

    def play(self):
        pass
