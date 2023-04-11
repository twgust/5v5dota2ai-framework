from bots.hero_bots.BaseHero import BaseHero
from game.player_hero import PlayerHero
from game.world import World


class HeroBotSkeleton(BaseHero):
    """Inherits BaseHero class"""
    _items = dict[int, str]

    def __init__(self):
        """Constructor, runs when class is initialised"""
        self.initialise_items()

    def initialise_items(self) -> None:
        """Initialise items that you want to buy here
        Key = priority, value = item name"""
        self._items = {1: 'power treads', 2: 'Maelstrom', 3: 'Dragon lance'}
        pass

    def get_move(self, hero: PlayerHero, game_ticks: int, world: World) -> None:
        """Here you should place the logic for how you want the hero to play"""
        pass
