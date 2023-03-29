from game.player_hero import PlayerHero
from game.world import World
from framework import RADIANT_TEAM, DIRE_TEAM


class sniper():
    _world: World
    _party: list[str]
    _heroes: list[PlayerHero]

    def get_move(self, hero: PlayerHero, game_ticks: int) -> None:
        if self._world.get_team() == RADIANT_TEAM:
            hero.move(500, 500, 0)
            if not hero.is_alive():
                hero.buyback()
            else:
                assert hero.get_buyback_cooldown_time() == 0
        if game_ticks > 100:
            print("woop woop")
