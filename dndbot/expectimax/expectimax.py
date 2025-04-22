from dndbot.expectimax.combat_state import CombatState
from dndbot.characters.combatant import CombatantState
from dndbot.characters.enemies.enemy_character import EnemyCharacter
from dndbot.characters.players.player_character import PlayerCharacter


class Expectimax:

    def __init__(self, players: list[PlayerCharacter], enemies: list[EnemyCharacter]):
        self.combatants = players + enemies
        initiatives = [(combatant.roll_initiative(), combatant) for combatant in self.combatants]
        initiatives.sort(reverse=True)
        self.turn_order = [combatant[1] for combatant in initiatives]
        initial_states = [CombatantState(c.name, c.hp_max, c.spell_slot_max) for c in self.combatants]
        self.root = CombatState(initial_states)

    def expand_subtree(self, node: CombatState, depth: int):
        current_layer = [node]
        next_layer = []
        for state in current_layer:
            state.expand_children()

    def play(self):
        pass
