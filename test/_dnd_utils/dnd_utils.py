from dndbot.characters.enemies.enemy_character import EnemyCharacter
from dndbot.characters.players.player_character import PlayerCharacter
from dndbot.dice.dice import D6, D12, D4
from dndbot.expectimax.actions.damage_data import DamageData
from dndbot.expectimax.actions.weapon_attack import WeaponAttack
from dndbot.expectimax.combat_state import CombatState


class DndUtils:

    @staticmethod
    def single_player_and_enemy_one_attack():
        player_damage = tuple([DamageData((1, D12), 1, 'bludgeoning')])
        player_attack = WeaponAttack('Melee', 4, player_damage)
        enemy_damage = tuple([DamageData((1, D6), 1, 'slashing')])
        enemy_attack = WeaponAttack('Melee', 4, enemy_damage)
        player = [PlayerCharacter({'name': 'p1', 'HP_Max': 20, 'AC': 16,
                                   'Actions': {'Weapon_Attacks': [player_attack]},
                                   'Initiative': 20, })]
        enemy = [EnemyCharacter({'name': 'e1', 'HP_Max': 10, 'AC': 12,
                                 'Actions': {'Weapon_Attacks': [enemy_attack]},
                                 'Initiative': 0})]
        return player, enemy

    @staticmethod
    def single_player_and_enemy():
        player_damage_1 = tuple([DamageData((1, D12), 1, 'bludgeoning')])
        player_attack_1 = WeaponAttack('Melee', 4, player_damage_1)
        player_damage_2 = tuple([DamageData((1, D6), 2, 'piercing')])
        player_attack_2 = WeaponAttack('Melee', 5, player_damage_2)

        enemy_damage_1 = tuple([DamageData((1, D6), 3, 'slashing')])
        enemy_attack_1 = WeaponAttack('Melee', 4, enemy_damage_1)
        enemy_damage_2 = tuple([DamageData((1, D4), 2, 'bludgeoning')])
        enemy_attack_2 = WeaponAttack('Ranged', 6, enemy_damage_2)

        player = [PlayerCharacter({'name': 'p1', 'HP_Max': 20, 'AC': 16,
                                   'Actions': {'Weapon_Attacks': [player_attack_1, player_attack_2]},
                                   'Initiative': 20, })]
        enemy = [EnemyCharacter({'name': 'e1', 'HP_Max': 10, 'AC': 12,
                                 'Actions': {'Weapon_Attacks': [enemy_attack_1, enemy_attack_2]},
                                 'Initiative': 0})]
        return player, enemy

    @staticmethod
    def print_state_tree(root: CombatState, probability=None, indent=''):
        print(indent, end='')
        if probability is not None:
            print(probability, root.combatant_states)
        else:
            print(root.combatant_states)
        for c in root.get_child_states():
            print(indent, '   ----')
            for s in c:
                DndUtils.print_state_tree(s[1], s[0], indent + '    ')

    @staticmethod
    def get_state_tree_string(root: CombatState, output_str: str, indent=''):
        output_str += indent
        output_str += str(root.combatant_states) + '\n'
        for c in root.get_child_states():
            output_str = DndUtils.get_state_tree_string(c[1], output_str, indent + '    ')
        return output_str

