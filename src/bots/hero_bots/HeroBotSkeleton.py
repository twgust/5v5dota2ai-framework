from bots.hero_bots.BaseHero import BaseHero
from game.player_hero import PlayerHero
from game.world import World


class HeroBotSkeleton(BaseHero):
    """Inherits BaseHero class"""
    _items = dict[int, str]
<<<<<<< Updated upstream
    _skill_build = dict[int, str]
=======
    _skill_build = dict[int, int]
>>>>>>> Stashed changes

    def __init__(self):
        """Constructor, runs when class is initialised"""
        self.initialise_items()
        self.initialise_skill_build()

    def initialise_skill_build(self):
<<<<<<< Updated upstream
        """Initialise the skill build here
        key = hero level, value = ability"""
        self._skill_build = {1, 'Ability'}
=======
        """
        Initialise the skill build here
        key = hero level, value = ability index
        Abilities indexes are counted from left to right as represented in the game.
        First ability has index 0, ultimate always has index 5.
        Aghanims shard and scepter abilities have indexes between ultimate ability and normal spells
        Talent tree specials have indexes >=9 and start from bottom right like this:
        16 - 15
        14 - 13
        12 - 11
        10 - 9
        This might not be true for every hero so you might have to try variations.
        This snippet can be used to find indices of abilities.
         for ability in hero.get_abilities():
                print(ability.get_ability_index())
                print(ability.get_name())
        """
        self._skill_build = {
            1: 0, 2: 0, 3: 0, 4: 0, 5: 0,
            6: 0, 7: 0, 8: 0, 9: 0, 10: 0,
            11: 0, 12: 0, 13: 0, 14: 0, 15: 0,
            16: 0, 17: 0, 18: 0, 19: 0, 20: 0,
            21: 0, 22: 0, 23: 0, 24: 0, 25: 0,
            26: 0, 27: 0, 28: 0, 29: 0, 30: 0
        }
>>>>>>> Stashed changes

    def initialise_items(self) -> None:
        """Initialise items that you want to buy here
        Key = priority, value = item name"""
        self._items = {1: 'item name', 2: 'item name', 3: 'item name'}
        pass

    def get_move(self, hero: PlayerHero, game_ticks: int, world: World) -> None:
        """Here you should place the logic for how you want the hero to play"""
        pass
