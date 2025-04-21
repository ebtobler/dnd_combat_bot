from abc import ABC

from dndbot.characters.combatant import Combatant
from dndbot.dice.dice import D20


class PlayerCharacter(Combatant, ABC):

    def __init__(self, stats: dict):
        self.stats = stats

    def __setitem__(self, k, v):
        self.stats[k] = v

    def __delitem__(self, v):
        del self.stats[v]

    def __getitem__(self, k):
        return self.stats[k]

    def __len__(self) -> int:
        return len(self.stats)

    def __iter__(self):
        return iter(self.stats)

    def __repr__(self):
        return self.stats['name']

    def roll_initiative(self):
        return next(iter(D20.roll(1))) + self.stats['Initiative']
