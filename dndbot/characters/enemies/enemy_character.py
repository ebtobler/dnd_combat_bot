from dndbot.characters.combatant import Combatant
from dndbot.dice.dice import D20
from dndbot.expectimax.actions.weapon_attack import WeaponAttack
from dndbot.input_parsing.string_parser import StringParser


class EnemyCharacter(Combatant):

    def __init__(self, stats: dict):
        self.team = 'enemy'
        self.name = stats.get('name')
        self.ac = stats.get('Armor Class')
        self.hp_max = stats.get('Hit Points')
        self.initiative = stats.get('Initiative')
        self.speed = stats.get('Speed')
        self.ability_scores = stats.get('Ability_Scores')
        self.saving_throws = stats.get('Saving_Throws')

        weapon_attacks = []
        if stats.get('Actions') is not None:
            for action_group in stats['Actions']:
                if action_group == 'Weapon_Attacks':
                    for attack_str in stats['Actions']['Weapon_Attacks']:
                        weapon_attacks.append(WeaponAttack(*StringParser.parse_player_attack_string(attack_str)))
        self.actions = stats.get('Actions')
        self.actions['Weapon_Attacks'] = weapon_attacks

        self.spells = stats.get('Spells')
        self.spell_slot_max = stats.get('Spell_Slots')
        if self.initiative is None:
            self.initiative = self.ability_scores['DEX_mod']

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name

    def __eq__(self, other):
        return isinstance(other, EnemyCharacter) and self.name == other.name

    def __lt__(self, other):
        return isinstance(other, Combatant) and self.ability_scores['DEX'] < other.ability_scores['DEX']

    def __hash__(self):
        return hash(self.name)

    def roll_initiative(self):
        return next(iter(D20.roll(1))) + self.initiative
