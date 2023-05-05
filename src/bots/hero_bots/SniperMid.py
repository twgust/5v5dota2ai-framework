from bots.hero_bots import ItemFunctions
from bots.hero_bots.BaseHero import BaseHero
from bots.hero_bots.SharedFunctions import SharedFunctions
from bots.test_bots import TestHeroTeam
from bots.test_bots.design.abstraction.Dota2Item import Dota2Item
from bots.test_bots.design.abstraction.ItemsList import ItemsList
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
    _dota_items = dict[int, Dota2Item]
    _items_list = ItemsList
    _skill_build = dict[int, int]
    _shared_functions = SharedFunctions()

    def __init__(self):
        self._items_list = ItemsList()
        self.initialise_items()
        self.initialise_skill_build()

    def initialise_skill_build(self):
        """create your custom skill build order for a hero"""
        self._skill_build = {
            1: 0, 2: 2, 3: 1, 4: 2, 5: 1,
            6: 5, 7: 1, 8: 2, 9: 2, 10: 0,
            11: 0, 12: 5, 13: 0, 14: 0, 15: 0,
            16: 0, 17: 0, 18: 5, 19: 0, 20: 0,
            21: 0, 22: 0, 23: 0, 24: 0, 25: 0,
            26: 0, 27: 0, 28: 0, 29: 0, 30: 0
        }

    def initialise_items(self) -> None:
        """create your custom item build for a hero"""
        self._items = {1: 'power treads', 2: 'Maelstrom', 3: 'Dragon lance', 4: 'Mjolnir', 5: 'Daedalus',
                       6: 'Monkey king bar', 7: 'Butterfly'}

        # _items_list is the master object you will interact with to access instances of Dota2Item/RecipeItem
        recipe_items = self._items_list.get_recipe_item_dict()
        self._dota_items = {1: recipe_items.get("item_bracer"),
                            2: recipe_items.get("item_maelstrom"),
                            3: recipe_items.get("item_dragon_lance"),
                            4: recipe_items.get("item_mjollnir"),
                            5: recipe_items.get("item_greater_crit"),
                            6: recipe_items.get("item_monkey_king_bar"),
                            7: recipe_items.get("item_butterfly")
                            }

    def get_move(self, hero: PlayerHero, game_ticks: int, world: World) -> None:
        """Get a move generated from this specific hero, takes the hero object and current world object as parameter"""
        # for v in hero.get_abilities():
        #   print(v.get_name(), v.get_ability_index(), v.get_ability_damage())
        if world.get_team() == RADIANT_TEAM:
            cord = self._shared_functions.get_pushing_creeps_for_lane_pos(hero, world, "mid")
            hero.move(cord.x, cord.y, cord.z)
            if not hero.is_alive():
                hero.buyback()
            else:
                assert hero.get_buyback_cooldown_time() == 0
            return
        # if self.level_up_ability(hero):
        #   return
        #   if self.cast_ability(hero, world):
        #     return
        if hero.get_gold() > 505:
            """ItemsList object is often used in conjunction with ItemFunctions, 
            below is an example implementation of buying the RecipeItem 'item_bracer'"""
            # step 1: acquire dictionary ref
            dic_ref = self._items_list.get_recipe_item_dict()
            # step 2: get item u want to buy
            recipe_item = dic_ref.get("item_bracer")
            # step 3: buy item
            ItemFunctions.buy_recipe_item(recipe_item, hero)
            return
        if self._shared_functions.attack_enemy_hero(hero, world):
            if self._shared_functions.attacked_by_tower(hero, world):
                pos = self._shared_functions.closest_friendly_tower(hero, world)
                # overwrite attack commando
                hero.move(pos.x, pos.y, pos.z)
            return
        if self._shared_functions.last_hit_creep(hero, world):
            return
        if self._shared_functions.deny_creep(hero, world):
            return


    def level_up_ability(self, hero: PlayerHero) -> bool:
        if hero.get_ability_points() > 0:
            hero.level_up(self._skill_build.get(hero.get_level()))
            return True
        return False

    def cast_ability(self, hero: PlayerHero, world: World) -> bool:
        """Cast an ability generated from this specific hero, takes the hero object and current world object as parameter"""
        enemy_hero = self._shared_functions.get_enemy_hero_to_attack(hero, world)
        ability = hero.get_abilities()[0]
        # Assassinate anyone
        enemy_heroes = self._shared_functions.get_enemy_heroes_within_specific_range(hero, world, 3000)
        if len(enemy_heroes) > 0:
            if ability.get_level() > 0:
                if ability.get_cooldown_time_remaining() == 0:
                    if hero.get_mana() > ability.get_mana_cost():
                        # hero.cast_target_unit(1, enemy_heroes[0])
                        hero.cast_target_area(0, hero.get_position())

                        print("casting A")
                        return True
            # Take aim
            ability = hero.get_abilities()[1]
            if ability.get_level() > 0:
                if ability.get_cooldown_time_remaining() == 0:
                    if hero.get_mana() > ability.get_mana_cost():
                        hero.cast_no_target(2)
                        print("casting B")

                        return True
        # Shrapnel
        ability = hero.get_abilities()[0]
        closest_enemy_creeps = self._shared_functions.get_closest_enemy_creeps(hero, world)
        if len(closest_enemy_creeps) >= 4:
            if ability.get_level() > 0:
                if ability.get_cooldown_time_remaining() == 0:
                    if hero.get_mana() > ability.get_mana_cost():
                        hero.cast_target_area(0, closest_enemy_creeps[0].get_position())
                        print("casting C")
                        return True
