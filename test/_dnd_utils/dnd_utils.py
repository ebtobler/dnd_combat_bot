from dndbot.characters.enemies.enemy_character import EnemyCharacter
from dndbot.characters.players.player_character import PlayerCharacter
from dndbot.dice.dice import D6, D12
from dndbot.expectimax.actions.damage_data import DamageData
from dndbot.expectimax.actions.weapon_attack import WeaponAttack
from dndbot.expectimax.combat_state import CombatState


class DndUtils:

    @staticmethod
    def single_player_and_enemy():
        player_damage = [DamageData((1, D12), 1, 'bludgeoning')]
        player_attack = WeaponAttack('Melee', 4, player_damage)
        enemy_damage = [DamageData((1, D6), 1, 'slashing')]
        enemy_attack = WeaponAttack('Melee', 4, enemy_damage)
        player = [PlayerCharacter({'name': 'p1', 'HP_Max': 20, 'AC': 16,
                                   'Actions': {'Weapon_Attacks': [player_attack]},
                                   'Initiative': 20, })]
        enemy = [EnemyCharacter({'name': 'e1', 'HP_Max': 10, 'AC': 12,
                                 'Actions': {'Weapon_Attacks': [enemy_attack]},
                                 'Initiative': 0})]
        return player, enemy

    @staticmethod
    def print_state_tree(root: CombatState, indent=''):
        print(indent, end='')
        print(root.combatant_states)
        for c in root.get_child_states():
            DndUtils.print_state_tree(c, indent + '    ')
