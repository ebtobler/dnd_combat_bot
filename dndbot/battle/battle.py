from dndbot.characters.combatant import Combatant
from dndbot.characters.enemies.enemy_character import EnemyCharacter
from dndbot.characters.players.player_character import PlayerCharacter


class Battle:

    def __init__(self, players: list[PlayerCharacter], enemies: list[EnemyCharacter]):
        self.players: list[PlayerCharacter] = players
        self.enemies: list[EnemyCharacter] = enemies
        self.combatants: list[Combatant] = players + enemies
        initiatives = [(combatant.roll_initiative(), combatant) for combatant in self.combatants]
        initiatives.sort(reverse=True)
        self.turn_order = [combatant[1] for combatant in initiatives]

