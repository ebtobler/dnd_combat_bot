from abc import ABC, abstractmethod

from dndbot.characters.combatant import Combatant


class Action(ABC):

    @abstractmethod
    def perform(self, target: Combatant):
        pass

    @abstractmethod
    def average_outcome(self, target: Combatant):
        pass
