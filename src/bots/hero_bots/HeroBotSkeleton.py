from bots.hero_bots.BaseHero import BaseHero
from game.player_hero import PlayerHero
from game.world import World

"""Inherits BaseHero class"""
class HeroBotSkeleton(BaseHero):

    """Initialise items that you want to buy here"""
    def initialise_items(self) -> None:
        pass

    '''Logic here'''
    def get_move(self, hero: PlayerHero, game_ticks: int, world: World) -> None:
        pass
