from abc import ABC, abstractmethod
from collections.abc import MutableMapping


class Combatant(ABC, MutableMapping):
    @abstractmethod
    def roll_initiative(self):
        pass
