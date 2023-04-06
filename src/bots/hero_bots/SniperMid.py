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

    def __init__(self):
        self.initialise_items()

    def initialise_items(self) -> None:
        _items = ['Power treads', 'Maelstrom', 'Dragon lance', 'Mjolnir', 'Daedalus', 'Monkey king bar', 'Butterfly',
                  'Eye of skadi']

    '''Get a move generated from this specific hero, takes the hero object and current world object as parameter'''

    def get_move(self, hero: PlayerHero, game_ticks: int, world: World) -> None:
        if world.get_team() == RADIANT_TEAM:
            hero.move(500, 500, 0)
            if not hero.is_alive():
                hero.buyback()
            else:
                assert hero.get_buyback_cooldown_time() == 0
        if game_ticks > 100:
            print("woop woop")
