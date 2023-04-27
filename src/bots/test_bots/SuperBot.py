from base_bot import BaseBot
from bots.test_bots.design.abstraction.Carry import Carry
from game.player_hero import PlayerHero
from game.world import World
from framework import RADIANT_TEAM, DIRE_TEAM
from bots.test_bots.design.abstraction.Dota2Item import Dota2Item

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
    "npc_dota_hero_invoker": {
        "agility"
    },
    "npc_dota_hero_lich": {
        "agility"
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
        "npc_dota_hero_invoker",
        "npc_dota_hero_lich",
    ],
}


class SuperBot(BaseBot):
    _world: World
    _party: list[str]
    _heroes: list[PlayerHero]
    _carries: list[Carry]
    _carries_dict: dict[str, Carry]

    def __init__(self, world: World) -> None:
        self._world = world
        print(world.get_team())
        self._party = party[world.get_team()]
        self._lane_tower_positions = {}
        self._carries = []
        self._carries_dict = {}

    def get_party(self) -> list[str]:
        return self._party

    def initialize(self, heroes: list[PlayerHero]):
        for hero in heroes:
            # get attribute from dictionary
            attribute = test.get(hero.get_name())
            if attribute.__contains__("agility"):
                my_hero = Carry(hero, attribute)
                self._carries_dict[hero.get_name()] = my_hero
                self._carries.append(my_hero)

    def actions(self, hero: PlayerHero, game_ticks: int):
        for ability in hero.get_abilities():
            print(ability.get_ability_index())
            print(ability.get_name())

        carry_hero = self._carries_dict.get(hero.get_name())
        if carry_hero is not None and game_ticks % 15 == 0:
            print("$$$ " + PlayerHero.get_name(hero) + " is buying items $$$")
            carry_hero.buy_items("carry")
        return
