from typing import Literal, TypedDict, Union, cast
from game.hero import Hero
from game.player_hero import PlayerHero
from game.unit import Unit
from game.world import World

''' 
    Class that contains functions that can be used by any bot or hero by importing the file.
    The functions are basic and meant as a starting point for bots to use.
'''


class SharedFunctions:
    def __init__(self):
        pass
    def attack_enemy_hero(self, hero: PlayerHero, world: World) -> bool:
        enemy_hero_to_attack = self.get_enemy_hero_to_attack(hero, world)
        if enemy_hero_to_attack is not None:
            hero.attack(enemy_hero_to_attack)
            return True
        return False

    def get_enemy_hero_to_attack(self, hero: PlayerHero, world: World) -> Union[Hero, None]:
        enemy_heroes: list[Hero] = self.get_closest_enemy_heroes(hero, world)
        heroes_with_hp: dict[Hero, int] = {}

        for enemy_hero in enemy_heroes:
            heroes_with_hp[enemy_hero] = enemy_hero.get_health()

        if len(heroes_with_hp) == 0:
            return

        return min(heroes_with_hp.keys(), key=(lambda enemy_hero: heroes_with_hp[enemy_hero]))

    def get_closest_enemy_heroes(self, hero: PlayerHero, world: World) -> list[Hero]:
        enemy_heroes: list[Hero] = world.get_enemy_heroes_of(hero)
        close_enemy_heroes: list[Hero] = []

        for enemy_hero in enemy_heroes:
            if world.get_distance_between_units(hero, enemy_hero) < 1250:
                close_enemy_heroes.append(enemy_hero)

        return close_enemy_heroes

    def get_enemy_heroes_within_specific_range(self, hero: PlayerHero, world: World, range: int) -> list[Unit]:
        enemy_heroes: list[Unit] = world.get_enemy_heroes_of(hero)
        units_within_range: list[Unit] = []

        for enemy_hero in enemy_heroes:
            if world.get_distance_between_units(hero, enemy_hero) < range:
                units_within_range.append(enemy_hero)

        return units_within_range

    def last_hit_creep(self, hero: PlayerHero, world: World) -> bool:
        creep_to_last_hit: Union[Unit, None] = self.get_creep_to_last_hit(hero, world)

        if creep_to_last_hit is not None:
            hero.attack(creep_to_last_hit)
            return True

        return False

    def get_creep_to_last_hit(self, hero: PlayerHero, world: World) -> Union[Unit, None]:
        closest_enemy_creeps = self.get_closest_enemy_creeps(hero, world)

        for creep in closest_enemy_creeps:
            if creep.get_health() < hero.get_attack_damage() + 40:
                return creep

    def get_closest_enemy_creeps(self, hero: PlayerHero, world: World) -> list[Unit]:
        creeps: list[Unit] = world.get_enemy_creeps_of(hero)
        close_enemy_creeps: list[Unit] = []

        for creep in creeps:
            if world.get_distance_between_units(hero, creep) < 500 or world.get_distance_between_units(hero,
                                                                                                       creep) < hero.get_attack_range():
                close_enemy_creeps.append(creep)

        return close_enemy_creeps

    def deny_creep(self, hero: PlayerHero, world: World) -> bool:
        creep_to_deny: Union[Unit, None] = self.get_creep_to_deny(hero, world)

        if creep_to_deny is not None:
            hero.attack(creep_to_deny)
            return True

        return False

    def get_creep_to_deny(self, hero: PlayerHero, world: World) -> Union[Unit, None]:
        closest_allied_creeps = self.get_closest_allied_creeps(hero, world)

        closest_allied_creeps.sort(key=lambda creep: world.get_distance_between_units(hero, creep))

        for creep in closest_allied_creeps:
            if creep.is_deniable() and creep.get_health() < hero.get_attack_damage() + 40:
                return creep

    def get_closest_allied_creeps(self, hero: PlayerHero, world: World) -> list[Unit]:
        creeps: list[Unit] = world.get_allied_creeps_of(hero)
        close_allied_creeps: list[Unit] = []

        for creep in creeps:
            if world.get_distance_between_units(hero, creep) < 600:
                close_allied_creeps.append(creep)

        return close_allied_creeps

    def is_near_allied_creeps(self, hero: PlayerHero, world: World) -> bool:
        allied_creeps: list[Unit] = world.get_allied_creeps_of(hero)
        close_allies: list[Unit] = world.get_allies_in_range_of(hero, 750)

        for ally in close_allies:
            if ally in allied_creeps:
                return True
        return False

    def get_closest_enemy(self, hero: PlayerHero, world: World) -> Union[Unit, None]:
        enemies: list[Unit] = self.get_closest_enemy_creeps(hero, world) + cast(list[Unit],
                                                                                self.get_closest_enemy_heroes(hero,
                                                                                                              world))
        enemies_with_distance_to_hero: dict[Unit, float] = {}

        for enemy in enemies:
            enemies_with_distance_to_hero[enemy] = world.get_distance_between_units(hero, enemy)

        return min(enemies_with_distance_to_hero.keys(),
                   key=(lambda allied_creep: enemies_with_distance_to_hero[allied_creep]), default=None)

    def get_closest_allied_creep(self, hero: PlayerHero, world: World) -> Unit:
        creeps: list[Unit] = world.get_allied_creeps_of(hero)
        creeps_with_distance_to_hero: dict[Unit, float] = {}

        for allied_creep in creeps:
            if allied_creep.get_name() == "npc_dota_ward_base":
                continue
            creeps_with_distance_to_hero[allied_creep] = world.get_distance_between_units(hero, allied_creep)

        return min(creeps_with_distance_to_hero.keys(),
                   key=(lambda allied_creep: creeps_with_distance_to_hero[allied_creep]))
