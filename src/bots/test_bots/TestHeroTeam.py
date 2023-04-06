from typing import Literal, TypedDict, Union, cast

from bots.hero_bots import SniperMid
from game.physical_entity import PhysicalEntity
from game.rune import Rune
from game.enums.ability_behavior import AbilityBehavior
from game.courier import Courier
from game.ability import Ability
from game.hero import Hero
from game.position import Position
from game.unit import Unit
from base_bot import BaseBot
from game.player_hero import PlayerHero
from game.world import World
from framework import RADIANT_TEAM, DIRE_TEAM
from bots.hero_bots import *

ARCANE: int = 0
PHASE: int = 1

TOP: int = 0
MID: int = 1
BOT: int = 2


class HeroData(TypedDict):
    boots: Union[Literal[0], Literal[1]]
    lane: Union[Literal[0], Literal[1], Literal[2]]


party: dict[int, dict[str, HeroData]] = {
    RADIANT_TEAM: {
        "npc_dota_hero_abaddon": {
            "boots": ARCANE,
            "lane": TOP,
        },
        "npc_dota_hero_axe": {
            "boots": PHASE,
            "lane": TOP,
        },
        "npc_dota_hero_sniper": {
            "boots": ARCANE,
            "lane": MID,
        },
        "npc_dota_hero_bane": {
            "boots": ARCANE,
            "lane": BOT,
        },
        "npc_dota_hero_disruptor": {
            "boots": ARCANE,
            "lane": BOT,
        },
    },
    DIRE_TEAM: {
        "npc_dota_hero_ancient_apparition": {
            "boots": ARCANE,
            "lane": TOP,
        },
        "npc_dota_hero_alchemist": {
            "boots": PHASE,
            "lane": TOP,
        },
        "npc_dota_hero_dragon_knight": {
            "boots": PHASE,
            "lane": MID,
        },
        "npc_dota_hero_ogre_magi": {
            "boots": ARCANE,
            "lane": BOT,
        },
        "npc_dota_hero_bristleback": {
            "boots": PHASE,
            "lane": BOT,
        },
    },
}

home_position = {
    RADIANT_TEAM: Position(-6774, -6311, 256),
    DIRE_TEAM: Position(6910, 6200, 256),
}

secret_shop_position = {
    RADIANT_TEAM: Position(-5077, 1893, 256),
    DIRE_TEAM: Position(4875, -1286, 256),
}


class TestHeroTeam(BaseBot):
    '''
    Tests:

    Basic AI.
    - Heroes buy boots of speed and extra town portal scroll at game start.
    - Heroes level up abilities. Will prioritize ultimates.
    - Heroes moves home when hp is less than 30 % of max hp.
    - Heroes moves back to fight when hp is greater than 90 % of max hp.
    - Heroes use town portal scroll to teleport to lane if at home, hp greater than 90 % of max hp and scroll is available.
    - Heroes attack enemy hero if enemy hero has less than 65 % of max hp. Will prioritize casting spells before normal attack.
    - Heroes attempt to get last hits and denies.
    - Heroes "hard"-flee when attacked by tower.
    - Heroes "soft"-flee when attacked by creeps or heroes.
    - Some heroes will buy energy booster using courier which delivers it to the hero to create arcane boots.
    - Heroes with arcane boots will use them when they've lost 175 mana or more.
    - Other heroes will buy blades of attack and chainmail using courier which delivers it to the hero to create phase boots.
    - Heroes with phase boots will use them whenever possible.
    '''

    _world: World
    _party: list[str]
    _heroes: list[PlayerHero]
    _should_move_home: dict[str, bool]
    _home_position: Position
    _secret_shop_position: Position
    _lane_tower_positions: dict[str, Position]
    _courier_moving_to_secret_shop: dict[str, bool]
    _courier_transferring_items: dict[str, bool]
    _go_aggressive_step1: bool
    _go_aggressive_step2: bool
    _sniper_obj: sniper.Sniper

    def __init__(self, world: World) -> None:
        team: int = world.get_team()

        self._world = world
        self._party = list(party[world.get_team()].keys())

    def get_party(self) -> list[str]:
        return self._party

    def initialize(self, heroes: list[PlayerHero]) -> None:
        self._heroes = heroes
        """#Initialise objects for heroes"""
        _sniper_obj = SniperMid.SniperMid()

    def initialize_lane_tower_positions(self) -> None:
        for lane_tower_name in [
            "dota_goodguys_tower1_top",
            "dota_goodguys_tower1_mid",
            "dota_goodguys_tower1_bot",
            "dota_goodguys_tower2_top",
            "dota_goodguys_tower2_mid",
            "dota_goodguys_tower2_bot",
            "dota_goodguys_tower3_top",
            "dota_goodguys_tower3_mid",
            "dota_goodguys_tower3_bot",
            "dota_badguys_tower1_top",
            "dota_badguys_tower1_mid",
            "dota_badguys_tower1_bot",
            "dota_badguys_tower2_top",
            "dota_badguys_tower2_mid",
            "dota_badguys_tower2_bot",
            "dota_badguys_tower3_top",
            "dota_badguys_tower3_mid",
            "dota_badguys_tower3_bot",
        ]:
            tower: Union[Unit, None] = self._world.get_unit_by_name(lane_tower_name)
            if tower is not None:
                self._lane_tower_positions[lane_tower_name] = tower.get_position()

    def before_actions(self, game_ticks: int) -> None:
        if (game_ticks % 100 == 0) and self._world.get_team() == 2:
            print("game_ticks:", game_ticks)

        if game_ticks == 1100:
            self._go_aggressive_step1 = True
        elif game_ticks == 1700:
            self._go_aggressive_step2 = True

    def actions(self, hero: PlayerHero, game_ticks: int) -> None:
        """#Check which hero logic to call"""
        if hero.get_name() == "npc_dota_hero_sniper":
            self._sniper_obj.get_move(hero, game_ticks, self._world)
