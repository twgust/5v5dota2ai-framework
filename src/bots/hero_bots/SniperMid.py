from bots.hero_bots.BaseHero import BaseHero
from bots.hero_bots.SharedFunctions import SharedFunctions
from bots.test_bots import TestHeroTeam
from game.player_hero import PlayerHero
from game.world import World
from framework import RADIANT_TEAM, DIRE_TEAM

'''Class representing a specific hero that can implement it's own logic
    Things to implement.
    1. Role?
    2. List of items to buy and order to buy?
'''


class SniperMid(BaseHero):
    _world: World
    _party: list[str]
    _heroes: list[PlayerHero]
    _items = dict[int, str]
    _skill_build = dict[int, int]
    _shared_functions = SharedFunctions()

    def __init__(self):
        self.initialise_items()
        self.initialise_skill_build()

    def initialise_skill_build(self):
        self._skill_build = {
            1: 1, 2: 2, 3: 1, 4: 2, 5: 1,
            6: 5, 7: 1, 8: 2, 9: 2, 10: 0,
            11: 0, 12: 5, 13: 0, 14: 0, 15: 0,
            16: 0, 17: 0, 18: 5, 19: 0, 20: 0,
            21: 0, 22: 0, 23: 0, 24: 0, 25: 0,
            26: 0, 27: 0, 28: 0, 29: 0, 30: 0
        }

    def initialise_items(self) -> None:
        self._items = {1: 'power treads', 2: 'Maelstrom', 3: 'Dragon lance', 4: 'Mjolnir', 5: 'Daedalus',
                       6: 'Monkey king bar', 7: 'Butterfly'}

    def get_move(self, hero: PlayerHero, game_ticks: int, world: World) -> None:
        """Get a move generated from this specific hero, takes the hero object and current world object as parameter"""
        # for v in hero.get_abilities():
        #   print(v.get_name(), v.get_ability_index(), v.get_ability_damage())
        if world.get_team() == RADIANT_TEAM:
            hero.move(500, 500, 0)
            if not hero.is_alive():
                hero.buyback()
            else:
                assert hero.get_buyback_cooldown_time() == 0
        if self.level_up_ability(hero):
            return
        if self.cast_ability(hero, world):
            return
        if hero.get_gold() > 505:
            return
        if self._shared_functions.attack_enemy_hero(hero, self._world):
            return
        if self._shared_functions.last_hit_creep(hero, self._world):
            return
        if self._shared_functions.deny_creep(hero, self._world):
            return

    def level_up_ability(self, hero: PlayerHero) -> bool:
        if hero.get_ability_points() > 0:
            hero.level_up(self._skill_build.get(hero.get_level()))
            return True
        return False

    def cast_ability(self, hero: PlayerHero, world: World) -> bool:
        """Cast an ability generated from this specific hero, takes the hero object and current world object as parameter"""
        enemy_hero = self._shared_functions.get_enemy_hero_to_attack(hero, world)
        ability = hero.get_abilities()[5]
        # Assassinate anyone
        enemy_heroes = self._shared_functions.get_enemy_heroes_within_specific_range(hero, world, 3000)
        if len(enemy_heroes) > 0:
            if ability.get_cooldown_time_remaining() == 0:
                if hero.get_mana() > ability.get_mana_cost():
                    hero.cast_target_unit(5, enemy_heroes[0])
                    return True
            # Take aim
            ability = hero.get_abilities()[2]
            if ability.get_cooldown_time_remaining() == 0:
                if hero.get_mana() > ability.get_mana_cost():
                    hero.cast_no_target(2)
                    return True
        # Shrapnel
        ability = hero.get_abilities()[0]
        closest_enemy_creeps = self._shared_functions.get_closest_enemy_creeps(hero, world)
        if len(closest_enemy_creeps) >= 4:
            if ability.get_cooldown_time_remaining() == 0:
                if hero.get_mana() > ability.get_mana_cost():
                    hero.cast_target_area(0, closest_enemy_creeps[0].get_position())
                    return True

