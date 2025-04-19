from dndbot.characters.players.character_creator import CharacterCreator

if __name__ == '__main__':
    new_character = CharacterCreator.get_stats_from_user()
    CharacterCreator.dump_character_to_json(new_character)
