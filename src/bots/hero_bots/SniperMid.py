from bots.hero_bots.BaseHero import BaseHero
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
    _items: list[str]
    _skill_build: dict[int, str]
    _items = dict[int, str]
    _skill_build = dict[int, int]


    def __init__(self):
        self.initialise_items()
        self.initialise_skill_build()
<<<<<<< Updated upstream
=======

    def initialise_skill_build(self):
        self._skill_build = {
            1: 1, 2: 2, 3: 1, 4: 2, 5: 1,
            6: 5, 7: 1, 8: 2, 9: 2, 10: 0,
            11: 0, 12: 5, 13: 0, 14: 0, 15: 0,
            16: 0, 17: 0, 18: 5, 19: 0, 20: 0,
            21: 0, 22: 0, 23: 0, 24: 0, 25: 0,
            26: 0, 27: 0, 28: 0, 29: 0, 30: 0
        }
>>>>>>> Stashed changes

    def initialise_items(self) -> None:
        self._items = {1: 'power treads', 2: 'Maelstrom', 3: 'Dragon lance', 4: 'Mjolnir', 5: 'Daedalus',
                       6: 'Monkey king bar', 7: 'Butterfly'}

    def initialise_skill_build(self):
        """Initialise the skill build here
        key = hero level, value = ability"""
        self._skill_build = {1, 'Ability'}

    def get_move(self, hero: PlayerHero, game_ticks: int, world: World) -> None:
<<<<<<< Updated upstream
        """Get a move generated from this specific hero, takes the hero object and current world object as parameter"""

=======
>>>>>>> Stashed changes
        if world.get_team() == RADIANT_TEAM:
            hero.move(500, 500, 0)
            if not hero.is_alive():
                hero.buyback()
            else:
                assert hero.get_buyback_cooldown_time() == 0
        if game_ticks > 100:
            print("woop woop")
        if self.level_up_ability(hero):
            return

    def level_up_ability(self, hero: PlayerHero) -> bool:
        if hero.get_ability_points() > 0:
            hero.level_up(self._skill_build.get(hero.get_level()))
            return True
        return False
