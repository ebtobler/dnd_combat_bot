from dndbot.battle.battle import Battle
from dndbot.battle.expectimax.combat_state import CombatState
from dndbot.characters.combatant import CombatantState


class Expectimax:

    def __init__(self, battle: Battle):
        self.battle = battle
        initial_states = [CombatantState(c['name'], c['HP'], c['Spell_Slots']) for c in battle.combatants]
        self.root = CombatState(initial_states)

    def generate_subtree(self, depth: int):
        pass

    def play(self):
        pass
