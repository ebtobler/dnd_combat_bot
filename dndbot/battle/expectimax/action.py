from abc import ABC, abstractmethod

from dndbot.characters.combatant import Combatant


class Action(ABC):

    @abstractmethod
    def generate_states(self, current_state: 'CombatState', target: Combatant):
        pass

    @abstractmethod
    def average_outcome(self, target: Combatant):
        pass
