from unittest import TestCase

from dndbot.battle.expectimax.expectimax import CombatState
from dndbot.characters.combatant import CombatantState
from dndbot.characters.enemies.enemy_character import EnemyCharacter
from dndbot.characters.players.player_character import PlayerCharacter


class TestCombatState(TestCase):

    def test_health_utility_function_for_single_state(self):
        combatants = [PlayerCharacter({'name': 'p1', 'HP_Max': 10}), PlayerCharacter({'name': 'p2', 'HP_Max': 15}),
                      EnemyCharacter({'name': 'e1', 'HP_Max': 4}), EnemyCharacter({'name': 'e2', 'HP_Max': 6})]
        combatant_states = {c: CombatantState(c.name, c.hp_max, c.spell_slot_max) for c in combatants}
        state = CombatState(combatant_states)
        expected_utility = 10 + 15 - 4 - 6
        result = state.utility()
        self.assertEqual(expected_utility, result)


class TestExpectimax(TestCase):
    pass
