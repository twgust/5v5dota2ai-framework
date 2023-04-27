from bots.hero_bots.BaseHero import BaseHero
from game.player_hero import PlayerHero
from game.world import World


class HeroBotSkeleton(BaseHero):
    """Inherits BaseHero class"""
    _items = dict[int, str]
    _skill_build = dict[int, str]

    def __init__(self):
        """Constructor, runs when class is initialised"""
        self.initialise_items()
        self.initialise_skill_build()

    def initialise_skill_build(self):
        """Initialise the skill build here
        key = hero level, value = ability"""
        self._skill_build = {1, 'Ability'}

    def initialise_items(self) -> None:
        """Initialise items that you want to buy here
        Key = priority, value = item name"""
        self._items = {1: 'item name', 2: 'item name', 3: 'item name'}
        pass

    def get_move(self, hero: PlayerHero, game_ticks: int, world: World) -> None:
        """Here you should place the logic for how you want the hero to play"""
        pass
