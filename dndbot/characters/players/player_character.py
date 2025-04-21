from dndbot.characters.combatant import Combatant
from dndbot.dice.dice import D20


class PlayerCharacter(Combatant):

    def __init__(self, stats: dict):
        self.name = stats['name']
        self.hp_max = stats['HP_Max']
        self.ac = stats['AC']
        self.initiative = stats['Initiative']
        self.speed = stats['Speed']
        self.ability_scores = stats['Ability_Scores']
        self.saving_throws = stats['Saving_Throws']
        self.actions = stats['Actions']
        self.spells = stats['Spells']

    def __repr__(self):
        return self.name

    def roll_initiative(self):
        return next(iter(D20.roll(1))) + self.initiative
