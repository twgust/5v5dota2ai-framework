from typing import Literal, TypedDict, Union, cast, Optional
from game.hero import Hero
from game.player_hero import PlayerHero
from game.position import Position
from game.tower import Tower
from game.unit import Unit
from game.world import World

''' 
    Class that contains functions that can be used by any bot or hero by importing the file.
    The functions are basic and meant as a starting point for bots to use. The purpose of the sample 
    implementations provided is to show how to use the game API to perform basic actions, as well as
    providing a starting point for bots to implement their own logic.
'''


class SharedFunctions:
    def __init__(self):
        pass

    def find_closest_unit(self, hero: PlayerHero, units: list[Unit], entity_accessor) -> Optional[Unit]:
        closest_unit = None
        closest_distance = float('inf')
        for unit in units:
            entity_value = entity_accessor(unit)
            if entity_value:
                distance_to_entity = self.distance_to(hero.get_position(), entity_value)
                if distance_to_entity < closest_distance:
                    closest_unit = unit
                    closest_distance = distance_to_entity
        return closest_unit

    def get_closest_unit(self, hero: PlayerHero, units: list[Unit]) -> Optional[Unit]:
        """
        Returns the closest unit from a list of units to the hero.
        """
        return self.find_closest_unit(hero, units, lambda unit: unit.get_position())

    def get_closest_unit_position(self, hero: PlayerHero, units: list[Unit]) -> Optional[Position]:
        """
        Returns the position of the closest unit from a list of units to the hero, convenience function
        since you can just call unit.get_position() on the returned unit to get position
        """
        return self.get_closest_unit(hero, units).get_position()

    def get_closest_allied_tower_position(self, hero: PlayerHero, world: World) -> Optional[Position]:
        """
        Tested
        """
        return self.get_closest_unit_position(hero, world.get_allied_towers_of(hero))

    def get_closest_allied_tower(self, hero: PlayerHero, world: World) -> Optional[Unit]:
        """
        Tested
        """
        return self.get_closest_unit(hero, world.get_allied_towers_of(hero))

    def get_closest_attacked_allied_tower(self, hero: PlayerHero, world: World) -> Optional[Unit]:
        """
        Tested
        """
        friendly_towers = world.get_allied_towers_of(hero)
        enemy_heroes = world.get_enemy_heroes_of(hero)
        attacked_towers = []
        for enemies in enemy_heroes:
            for tower in friendly_towers:
                if enemies.get_attack_target() == tower.get_id():
                    attacked_towers.append(tower)
        if attacked_towers:
            return self.get_closest_unit(hero, attacked_towers)
        else:
            return None

    def get_closest_attacked_enemy_hero(self, hero: PlayerHero, world: World) -> Optional[Unit]:
        """
        Tested
        """
        enemies = world.get_enemy_heroes_of(hero)
        for enemy in enemies:
            if not enemy.get_has_aggro():
                enemies.remove(enemy)
        # to get the location, you can simply call enemy.get_position() on the returned unit
        return self.get_closest_unit(hero, enemies)

    def is_enemy_hero_in_enemy_tower_range(self, hero: PlayerHero, world: World) -> bool:
        """
        Returns true if the enemy hero is under a tower
        Tested
        """
        enemy_heroes = world.get_enemy_heroes_of(hero)
        enemy_towers = world.get_enemy_heroes_of(hero)
        closest_enemy_hero = self.get_closest_unit(hero, enemy_heroes)
        if closest_enemy_hero:
            for enemy_tower in enemy_towers:
                enemy_tower.get_attack_range()
                if enemy_tower.get_position():
                    if self.distance_to(closest_enemy_hero.get_position(), enemy_tower.get_position()) \
                            < enemy_tower.get_attack_range():
                        return True
        return False

    def get_closest_enemy_building(self, hero: PlayerHero, world: World) -> Optional[Unit]:
        return self.get_closest_unit(hero, world.get_enemy_towers_of(hero))

    def get_weakest_unit(units: list[Unit]) -> Optional[Unit]:
        """
        Finds the unit with the lowest damage among a list of units and returns it..
        """
        weakest_unit = None
        lowest_damage = float('inf')
        for unit in units:
            if isinstance(unit, Unit):
                unit_damage = unit.get_attack_damage()
                if unit_damage < lowest_damage:
                    weakest_unit = unit
                    lowest_damage = unit_damage
        return weakest_unit

    def get_lowest_health_unit(self, units: list[Unit]) -> Optional[Unit]:
        """
        Finds the unit with the lowest health among a list of units and returns it.
        """
        lowest_health_unit = None
        lowest_health = float('inf')
        for unit in units:
            if isinstance(unit, Unit):
                unit_health = unit.get_health()
                if unit_health < lowest_health:
                    lowest_health_unit = unit
                    lowest_health = unit_health
        return lowest_health_unit

    def get_pushing_creeps_position(self, hero: Hero, world: World, target_lane: str):
        friendly_creeps = world.get_allied_creeps_of(hero)
        closest_creep = None
        closest_distance = float('inf')
        closest_enemy_tower_mid = self.get_closest_enemy_tower_for_lane_position(hero, world, target_lane)

        for creep in friendly_creeps:
            creep_position = creep.get_position()
            if creep_position:
                distance_to_creep = world.get_distance_between_positions(closest_enemy_tower_mid, creep_position)
                if distance_to_creep < closest_distance:
                    closest_creep = creep_position
                    closest_distance = distance_to_creep
        return closest_creep

    def get_closest_enemy_tower_for_lane_position(self, hero: Hero, world: World, target_lane: str) -> Position:
        enemy_towers = world.get_enemy_towers_of(hero)
        for tower in enemy_towers:
            if target_lane in tower.get_name():
                return tower.get_position()

    def get_closest_enemy_tower_for_lane(self, hero: Hero, world: World, target_lane: str) -> Tower:
        enemy_towers = world.get_enemy_towers_of(hero)
        for tower in enemy_towers:
            if target_lane in tower.get_name():
                return tower

    def distance_to(self, hero_position: Position, other: Position) -> float:
        return ((hero_position.x - other.x) ** 2 + (hero_position.y - other.y) ** 2 + (
                hero_position.z - other.z) ** 2) ** 0.5

    def attacked_by_tower(self, hero, world) -> bool:
        towers = world.get_enemy_towers_of(hero)
        for tower in towers:
            entity = world.get_entity_by_id(tower.get_attack_target())
            if isinstance(entity, PlayerHero):
                if entity.__eq__(hero):
                    print(entity.get_name())
                    return True
                else:
                    return False

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
