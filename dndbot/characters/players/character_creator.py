from dndbot.characters.players.player_character import PlayerCharacter
from os import path
from json import dump

class CharacterCreator:

    @staticmethod
    def get_stat_group(attr_group: list[str]) -> dict:
        attrs = {}
        for field in attr_group:
            user_input = input(f'{field}: ')
            if user_input == 'x':
                return {}
            attrs[field] = user_input
        return attrs

    @staticmethod
    def get_stats_from_user() -> PlayerCharacter:
        name = ['Name']
        armor_class = ['Armor Class']
        max_hp = ['Max HP']
        initiative = ['Initiative']
        speed = ['Speed']
        prof_bonus = ['Proficiency Bonus']
        spell_dc = ['Spell DC']
        ability_scores = ['Strength, mod', 'Dexterity, mod', 'Constitution, mod',
                      'Intelligence, mod', 'Wisdom, mod', 'Charisma, mod']
        saves = ['Str save', 'Dex save', 'Con save', 'Int save', 'Wis save', 'Cha save']
        actions = ['Actions']
        bonus_actions = ['Bonus Actions']
        spell_slots = ['lvl 1 spell slots', 'lvl 2 spell slots', 'lvl 3 spell slots']
        spells = ['Cantrips', 'lvl 1 spells', 'lvl 2 spells', 'lvl 3 spells']

        group_key = {
            name: 'name',
            armor_class: 'AC',
            max_hp: 'HP_Max',
            initiative: 'Initiative',
            speed: 'Speed',
            prof_bonus: 'Proficiency_Bonus',
            spell_dc: 'Spell_DC',
            ability_scores: 'Ability_Scores',
            saves: 'Saving_Throws',
            actions: 'Actions',
            bonus_actions: 'Bonus Actions',
            spell_slots: 'Spell_Slots',
            spells: "Spells"
        }

        to_read = [name, armor_class, max_hp, initiative, speed, prof_bonus, spell_dc,
                   ability_scores, saves, actions, bonus_actions, spell_slots, spells]

        stats = {}

        print("Creating a new character (type 'x' to exit):")
        for group in to_read:
            value = CharacterCreator.get_stat_group(group)
            if len(value) == 0:
                return PlayerCharacter({})

            if len(value) == 1:
                value = next(iter(value.values()))
            stats[group_key[group]] = value

        return PlayerCharacter(stats)

    @staticmethod
    def dump_character_to_json(char_stats: PlayerCharacter):
        character_file = path.join(path.abspath(__file__), '..', '..', '..', 'stats', 'players', f'{char_stats["name"]}.json')
        with open(character_file, 'w') as f:
            dump(char_stats, f, indent=2)
