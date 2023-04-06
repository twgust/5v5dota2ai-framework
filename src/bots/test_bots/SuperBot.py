from base_bot import BaseBot
from bots.test_bots.design.abstraction.Carry import Carry
from game.player_hero import PlayerHero
from game.world import World
from framework import RADIANT_TEAM, DIRE_TEAM

from game.unit import Unit
from typing import Union, Literal, TypedDict
from game.position import Position

test: dict[str, dict[str]] = {
    "npc_dota_hero_sniper": {
        "agility"
    },
    "npc_dota_hero_arc_warden": {
        "agility"
    },
    "npc_dota_hero_bloodseeker": {
        "agility"
    },
    "npc_dota_hero_bounty_hunter": {
        "agility"
    },
    "npc_dota_hero_broodmother": {
        "agility"
    },
    "npc_dota_hero_clinkz": {
        "agility"
    },
    "npc_dota_hero_drow_ranger": {
        "agility"
    },
    "npc_dota_hero_ember_spirit": {
        "agility"
    },
    "npc_dota_hero_faceless_void": {
        "agility"
    },
    "npc_dota_hero_lich": {
        "intelligence"
    },
}
party = {
    RADIANT_TEAM: [
        "npc_dota_hero_sniper",
        "npc_dota_hero_arc_warden",
        "npc_dota_hero_bloodseeker",
        "npc_dota_hero_bounty_hunter",
        "npc_dota_hero_broodmother",
    ],
    DIRE_TEAM: [
        "npc_dota_hero_clinkz",
        "npc_dota_hero_drow_ranger",
        "npc_dota_hero_ember_spirit",
        "npc_dota_hero_faceless_void",
        "npc_dota_hero_lich",
    ],
}


class SuperBot(BaseBot):
    _world: World
    _party: list[str]
    _heroes: list[PlayerHero]
    _carries: list[Carry]

    def __init__(self, world: World) -> None:
        self._world = world
        print(world.get_team())
        self._party = party[world.get_team()]
        self._lane_tower_positions = {}
        self._carries = []

    def get_party(self) -> list[str]:
        return self._party

    def initialize(self, heroes: list[PlayerHero]):
        for hero in heroes:
            attribute = test.get(hero.get_name())
            if attribute.__contains__("agility"):
                my_hero = Carry(hero.get_name(), attribute)
                self._carries.append(my_hero)
        for carry in self._carries:
            print(carry.hero_name)

    def actions(self, hero: PlayerHero, game_ticks: int):
        return
