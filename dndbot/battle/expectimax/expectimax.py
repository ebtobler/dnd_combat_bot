from dndbot.battle.battle import Battle
from dndbot.characters.combatant import CombatantState, Combatant


class CombatState:

    def __init__(self, combatant_states: dict[Combatant: CombatantState]):
        self.combatant_states = combatant_states


class Expectimax:

    def __init__(self, battle: Battle):
        self.battle = battle
        initial_states = [CombatantState(c['name'], c['HP'], c['Spell_Slots']) for c in battle.combatants]
        self.root = CombatState(initial_states)

    def generate_subtree(self, depth: int):
        pass

    def play(self):
        pass
