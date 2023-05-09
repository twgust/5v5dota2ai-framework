# Strength Carry items
from typing import List


# Agility Carry items
# 1) Divine Rapier
# 2) Mjolnir
# 3) Manta Style
# 4) Butterfly
# 5) Daedalus

# Intelligence Carry items
# 1) Divine Rapier


# Strength Support items

# Agility Support items

# Intelligence Support items

# class which represents a dota 2 item
# contains functions to get the item's name, cost, hasActiveEffect, getActiveEffect,
# and Role (Carry, Support, etc.),
# and Attribute (Strength, Agility, Intelligence)
class Dota2Item:
    def __init__(self, name: str, cost: int, hasActiveEffect: bool, active_effect: str, attribute: dict[str, str]) -> None:
        self.name = name
        self.cost = cost
        self.is_active = hasActiveEffect
        self.activeEffect = active_effect
        self.role = self.determine_role()
        self.attribute = attribute

    def determine_role(self) -> str: return "Carry"

    def get_name(self) -> str: return self.name

    def get_cost(self) -> int: return self.cost

    def has_active_effect(self) -> bool: return self.has_active_effect

    def get_active_effect(self) -> str: return self.activeEffect

    def get_role(self) -> str: return self.role

    def get_attribute(self) -> list[str]: return self.attribute

    def to_string(self) -> str: return "NAME: " + self.name + ", COST: " + str(self.cost) + ", ATTRIBUTES " + ", ".join([str(x) for x in self.attribute])

    def __eq__(self, other):
        return (self.name, self.cost) == (other.name, other.cost)

