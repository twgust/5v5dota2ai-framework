from abc import abstractmethod
from game.player_hero import PlayerHero
from game.world import World


class BaseHero:

    @abstractmethod
    def initialise_items(self) -> None:
        pass

    @abstractmethod
    def get_move(self, hero: PlayerHero, game_ticks: int, world: World) -> None:
        pass
