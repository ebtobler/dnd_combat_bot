from dndbot.characters.combatant import Combatant
from dndbot.dice.dice import D20


class EnemyCharacter(Combatant):

    def __init__(self, stats: dict):
        self.team = 'enemy'
        self.name = stats.get('name')
        self.hp_max = stats.get('HP_Max')
        self.ac = stats.get('AC')
        self.initiative = stats.get('Initiative')
        self.speed = stats.get('Speed')
        self.ability_scores = stats.get('Ability_Scores')
        self.saving_throws = stats.get('Saving_Throws')
        self.actions = stats.get('Actions')
        self.spells = stats.get('Spells')
        self.spell_slot_max = stats.get('Spell_Slots')

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name

    def roll_initiative(self):
        return next(iter(D20.roll(1))) + self.initiative
