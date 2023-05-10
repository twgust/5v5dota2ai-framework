from enum import Enum

from bots.hero_bots.Dota2ItemAttribute import Dota2Attribute
from bots.hero_bots.Dota2PlayerHeroRole import Dota2Role
from bots.test_bots.design.abstraction.Dota2Item import Dota2Item
from bots.test_bots.design.abstraction.ItemsList import ItemsList
from bots.test_bots.design.abstraction.RecipeItem import RecipeItem
from game.player_hero import PlayerHero
from pprint import pprint


def generate_item_list(item: RecipeItem) -> list:
    components = item.get_required_items()
    item_names_list = list(component.name for component in components)
    return item_names_list


def attempt_item_purchase(item: Dota2Item, hero: PlayerHero) -> bool:
    """
    Attempts to purchase a single item.
    Parameters:
    item (Dota2Item): The item to be purchased.
    Returns:
    bool: True if the purchase was successful, False otherwise.
    """
    if hero.get_gold() > item.cost:
        hero.buy(item.name)
        return True
    else:
        # item is too expensive so we return false
        return False


def attempt_partial_item_purchase(item: RecipeItem, hero: PlayerHero) -> bool:
    """
    Attempts to purchase a partial item using its recipe.
    Parameters:
    item (RecipeItem): The recipe of the item to be purchased.
    Returns:
    bool: True if the purchase was successful, False otherwise.
    """
    for component in item.get_required_items():
        if component.name not in [item.name for item in hero.get_items()]:
            if attempt_item_purchase(component, hero):
                return True
    return False


def attempt_complete_item_purchase(item: RecipeItem, hero: PlayerHero) -> bool:
    """
    Attempts to purchase a complete item using its recipe.
    Parameters:
    item (RecipeItem): The recipe of the item to be purchased.
    Returns:
    bool: True if the purchase was successful, False otherwise.
    """
    components = generate_item_list(item)
    if hero.get_gold() > item.cost:
        hero.buy_combined(components)
        return True
    else:
        return False


def buy_recipe_item(item: RecipeItem, hero: PlayerHero) -> bool:
    """
        This function attempts to buy a recipe item by first checking if the player can afford to buy the complete item
        using `attempt_complete_item_purchase`, and if not, it attempts to buy the item's required components using
        `attempt_partial_item_purchase`. If the purchase is successful, it returns `True`, else it returns `False`.

        :param item: A `RecipeItem` object representing the item to be purchased.
        :param hero: An instanceo of a PlayerHero
        :return: A boolean value indicating whether the purchase was successful.
        """
    # components = item.get_required_items()
    buy_status = attempt_complete_item_purchase(item, hero)
    if not buy_status:
        return attempt_partial_item_purchase(item, hero)
    elif buy_status:
        return buy_status


def buy_max_build_item(potential_items: list[Dota2Item], hero: PlayerHero) -> bool:
    """
    This function buys the highest-cost item that a player can afford,
    among the potential items passed in the argument, for the given hero.
    It takes a list of potential_items (a list of Dota2Item objects) and a hero (a PlayerHero object)
    as input parameters and returns a boolean value indicating if the purchase was successful or not.

    :param potential_items: A list of potential Dota2Item objects that the hero can buy.
    :param hero: A PlayerHero object representing the hero who wants to buy the item.
    """
    if potential_items:
        max_cost_item = max(potential_items,
                            key=lambda item: item.cost if item.cost <= hero.get_gold() else float('-inf'))
        if max_cost_item is not None:
            if max_cost_item.name not in [item.name for item in hero.get_items()]:
                if isinstance(max_cost_item, RecipeItem):
                    hero.buy_combined(generate_item_list(max_cost_item))
                else:
                    hero.buy(max_cost_item.name)
                return True
    return False


def buy_suitable_item(hero: PlayerHero, role: Dota2Role, item_lists: ItemsList, attribute: Dota2Attribute) -> bool:
    items = []
    if role == Dota2Role.CARRY:
        items = item_lists.get_carry_items()
    elif role == Dota2Role.SUPPORT:
        items = item_lists.get_support_items()
    else:
        return False
    calculate_highest_score(hero, items, role, attribute)
    return True


def calculate_highest_score(hero: PlayerHero, item_list: list[Dota2Item], role: Dota2Role,
                            attribute: Dota2Attribute) -> float:
    """
    This function calculates the highest score among the items in the item_list passed in the argument,
    for the given hero. It takes a list of potential_items (a list of Dota2Item objects) and a hero (a PlayerHero object)
    as input parameters and returns a boolean value indicating if the purchase was successful or not.

    :param potential_items: A list of potential Dota2Item objects that the hero can buy.
    :param hero: A PlayerHero object representing the hero who wants to buy the item.
    """
    if item_list:
        max_score_item = max(item_list, key=lambda item: calculate_item_score(hero, item, role, attribute))
        if max_score_item is not None:
            if max_score_item.name not in [item.name for item in hero.get_items()]:
                if isinstance(max_score_item, RecipeItem):
                    hero.buy_combined(generate_item_list(max_score_item))
                else:
                    hero.buy(max_score_item.name)
                return True
    return False


def calculate_item_score(hero: PlayerHero, item: Dota2Item, role: Dota2Role, attribute: Dota2Attribute) -> float:
    """
    hero (PlayerHero): The hero who's doing the purchasing
    item (Dota2Item): The item that the hero wishes to purchase
    role (Dota2Role): The role of the hero
    attribute (Dota2Attribute): The attribute that the hero wishes to prioritize
    """
    if role == Dota2Role.CARRY:
        return calculate_carry_item_score(hero, item, attribute)
    elif role == Dota2Role.SUPPORT:
        return calculate_support_item_score(hero, item, attribute)
    return 0


def calculate_carry_item_score(hero: PlayerHero, item: Dota2Item, attribute: Dota2Attribute) -> float:
    """
    hero (PlayerHero): The hero who's doing the purchasing
    item (Dota2Item): The item that the hero wishes to purchase
    attribute (Dota2Attribute): The attribute that the hero wishes to prioritize
    """
    score = 0
    bonus_damage_weight = 2.0
    # Add 2 points for every point of the desired attribute
    if str(attribute.value) in item.attribute.keys():
        score += float(item.attribute[str(attribute.value)]) * 2

    # Add 2 points for every bonus damage point
    if "bonus_damage" in item.attribute.keys():
        score += bonus_damage_weight

    # Add 1 point for every 10 attack speed points
    if "bonus_attack_speed" in item.attribute.keys():
        score += float(item.attribute["bonus_attack_speed"]) // 10

    # Add 1 point for every 3% lifesteal
    if "lifesteal_percent" in item.attribute.keys():
        score += float(item.attribute["lifesteal_percent"]) // 3

    # Add 1 point for every 3 points of armor
    if "bonus_armor" in item.attribute.keys():
        score += float(item.attribute["bonus_armor"]) // 3
    return score


def calculate_support_item_score(hero: PlayerHero, item: Dota2Item) -> float:
    return 0
