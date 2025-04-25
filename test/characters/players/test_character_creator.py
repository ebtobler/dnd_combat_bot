from os import path, remove
from unittest import TestCase

from dndbot.characters.players.character_creator import CharacterCreator
from dndbot.characters.players.player_character import PlayerCharacter


class TestCharacterCreator(TestCase):

    def test_dump_character_to_json(self):
        character = PlayerCharacter({'name': 'test', 'AC': 10})
        CharacterCreator.dump_character_to_json(character)
        test_character_file = path.join(path.dirname(__file__), '..', '..', '..', 'stats', 'players', 'test.json')
        if path.exists(test_character_file):
            remove(test_character_file)
        else:
            self.fail()
