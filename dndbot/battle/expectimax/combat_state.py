from dndbot.characters.combatant import Combatant, CombatantState


class CombatState:

    def __init__(self, combatant_states: dict[Combatant: CombatantState]):
        self.combatant_states = combatant_states

