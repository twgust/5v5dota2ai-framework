from enum import Enum

from bots.hero_bots.Dota2ItemAttribute import Dota2Attribute
from bots.hero_bots.Dota2PlayerHeroRole import Dota2Role
from bots.test_bots.design.abstraction.Dota2Item import Dota2Item
from bots.test_bots.design.abstraction.ItemsList import ItemsList
from bots.test_bots.design.abstraction.RecipeItem import RecipeItem
from game.courier import Courier
from game.item import Item
from game.player_hero import PlayerHero
from pprint import pprint
from collections import Counter

from game.world import World


def generate_item_components_list(item: RecipeItem, hero_items: list[Item]) -> list:
    """
    This function generates a list of item components that are required to purchase a recipe item.
    Checks item for sub-recipe items and adds their components to the list.
    Checks if hero has the required components and adds them to the list if they are missing.
    Parameters:
    item (RecipeItem): The RecipeItem to be purchased.
    hero_items (list[Item]): The items that the hero currently owns.
    Returns:
    list: A list of item components that are required to purchase a recipe item.
    """
    required_components = []
    for component in item.get_required_items():
        if isinstance(component, RecipeItem):
            for sub_component in component.get_required_items():
                required_components.append(sub_component)
        else:
            required_components.append(component)
    hero_component_counts = Counter(component.name for component in hero_items)
    required_component_counts = Counter(component.name for component in required_components)
    item_names_list = []

    for component_name, required_count in required_component_counts.items():
        owned_count = hero_component_counts[component_name]

        if owned_count < required_count:
            missing_count = required_count - owned_count
            item_names_list.extend([component_name] * missing_count)

    pprint(item_names_list)
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


def get_all_the_items(hero: PlayerHero, world: World) -> list:
    item_list = []
    courier = world.get_entity_by_id(hero.get_courier_id())
    if isinstance(courier, Courier):
        item_list += [item for item in courier.get_items()]
    item_list += [item for item in hero.get_items()]
    return item_list


def attempt_complete_item_purchase(item: RecipeItem, hero: PlayerHero, world: World) -> bool:
    """
    Attempts to purchase a complete item using its recipe.
    Parameters:
    item (RecipeItem): The recipe of the item to be purchased.
    Returns:
    bool: True if the purchase was successful, False otherwise.
    """

    components = generate_item_components_list(item, get_all_the_items(hero, world))
    if hero.get_gold() > item.cost:
        hero.buy_combined(components)
        return True
    else:
        return False


def buy_recipe_item(item: RecipeItem, hero: PlayerHero, world: World) -> bool:
    """
        This function attempts to buy a recipe item by first checking if the player can afford to buy the complete item
        using `attempt_complete_item_purchase`, and if not, it attempts to buy the item's required components using
        `attempt_partial_item_purchase`. If the purchase is successful, it returns `True`, else it returns `False`.

        :param item: A `RecipeItem` object representing the item to be purchased.
        :param hero: An instanceo of a PlayerHero
        :return: A boolean value indicating whether the purchase was successful.
        """
    # components = item.get_required_items()
    buy_status = attempt_complete_item_purchase(item, hero, world)
    if not buy_status:
        return attempt_partial_item_purchase(item, hero)
    elif buy_status:
        return buy_status


def can_afford_item(item: Dota2Item, hero: PlayerHero) -> bool:
    """
    This function checks if the given hero can afford to buy the given item.
    It takes a hero (a PlayerHero object) and an item (a Dota2Item object) as input parameters
    and returns a boolean value indicating if the hero can afford to buy the item or not.
    """
    if hero.get_gold() > item.cost:
        return True
    return False


def item_in_inventory(item: Dota2Item, hero: PlayerHero) -> bool:
    """
    This function checks if the given hero has the given item in their inventory.
    It takes a hero (a PlayerHero object) and an item (a Dota2Item object) as input parameters
    and returns a boolean value indicating if the item is in the hero's inventory or not.
    """
    if item.name in [item.name for item in hero.get_items()]:
        return True
    return False


def buy_max_build_item(potential_items: list[Dota2Item], hero: PlayerHero, world: World) -> bool:
    """
    This function buys the highest-cost item that a player can afford,
    among the potential items passed in the argument, for the given hero.
    It takes a list of potential_items (a list of Dota2Item objects) and a hero (a PlayerHero object)
    as input parameters and returns a boolean value indicating if the purchase was successful or not.

    :param potential_items: A list of potential Dota2Item objects that the hero can buy.
    :param hero: A PlayerHero object representing the hero who wants to buy the item.
    :param world: A world object representing the world in game state
    """
    if potential_items:
        max_cost_item = max(potential_items,
                            key=lambda item: item.cost if can_afford_item(item, hero) else float('-inf'))
        if max_cost_item is not None:
            if not item_in_inventory(max_cost_item, hero):
                if isinstance(max_cost_item, RecipeItem):
                    hero.buy_combined(generate_item_components_list(max_cost_item, get_all_the_items(hero, world)))
                else:
                    hero.buy(max_cost_item.name)
                return True
    return False


def has_item(unit_expression, item: Dota2Item) -> bool:
    if item.name in [item.name for item in unit_expression]:
        return True


def my_test(hero: PlayerHero, item: Dota2Item, world: World) -> bool:
    courier = world.get_entity_by_id(hero.get_courier_id())
    if isinstance(courier, Courier):
        return has_item(courier.get_items(), item)


def hero_has_item(hero: PlayerHero, item: Dota2Item) -> bool:
    """
    This function checks if the given hero has the given item in their inventory.
    It takes a hero (a PlayerHero object) and an item (a Dota2Item object) as input parameters
    and returns a boolean value indicating if the item is in the hero's inventory or not.
    """
    if item.name in [item.name for item in hero.get_items()]:
        return True
    return False


def courier_has_item(hero: PlayerHero, item: Dota2Item, world: World) -> bool:
    courier = world.get_entity_by_id(hero.get_courier_id())
    if isinstance(courier, Courier):
        if item.name in [item.name for item in courier.get_items()]:
            return True
    return False



def get_affordable_items(hero: PlayerHero, items: list[Dota2Item]) -> list[Dota2Item]:
    """
    This function returns a list of items that the hero can afford to buy.
    It takes a hero (a PlayerHero object) and a list of items (a list of Dota2Item objects) as input parameters
    and returns a list of affordable items (a list of Dota2Item objects).
    """
    affordable_items = [item for item in items if item.get_cost() <= hero.get_gold()]
    pprint(affordable_items)
    return affordable_items


def courier_to_secret_shop(hero: PlayerHero, world: World) -> bool:
    courier = world.get_entity_by_id(hero.get_courier_id())
    assert courier is not None
    if isinstance(courier, Courier):
        if hero.get_courier_transferring_items():
            print(hero.get_name() + " >>courier already transferring items")
            return False
        if hero.get_courier_moving_to_secret_shop():
            print(hero.get_name() + " >>courier already moving to secret shop!")
            return True
        else:
            print(hero.get_name() + " >> courier was idle, now moving to secret shop!")
            hero.courier_secret_shop()
            hero.set_courier_moving_to_secret_shop(True)
            hero.set_courier_transferring_items(False)
            return True


def buy_secret_shop_item(hero: PlayerHero, item: Dota2Item, world: World) -> bool:
    courier = world.get_entity_by_id(hero.get_courier_id())
    assert courier is not None
    if isinstance(courier, Courier):
        if courier.is_in_range_of_secret_shop():
            print("buy secret item")


def buy_suitable_item(hero: PlayerHero, role: Dota2Role, attributes: list[Dota2Attribute],
                      item_lists: ItemsList, world: World) -> bool:
    items = []
    if role == Dota2Role.CARRY:
        items = item_lists.get_carry_items()
    elif role == Dota2Role.SUPPORT:
        items = item_lists.get_support_items()
    elif role == Dota2Role.UTILITY:
        items = item_lists.get_utility_items()
    else:
        return False

    return buy_highest_score_item(hero, role, attributes, items, world)

def get_courier(hero: PlayerHero, world: World) -> Courier:
    courier = world.get_entity_by_id(hero.get_courier_id())
    assert courier is not None
    if isinstance(courier, Courier):
        return courier


def is_item_secret_shop(item: RecipeItem) -> bool:
    for comp in item.get_required_items():
        if comp.secret_shop:
            return True
    return False


def item_component_of_item(item: Dota2Item, target_items: list[Dota2Item]) -> RecipeItem:
    for targets in target_items:
        if isinstance(targets, RecipeItem):
            for comp in targets.get_required_items():
                if comp.name == item.name:
                    return targets
    return None


def buy_highest_score_item(hero: PlayerHero, role: Dota2Role, attributes: list[Dota2Attribute],
                           item_list: list[Dota2Item], world: World) -> bool:
    """
    This function calculates the highest score among the items in the item_list passed in the argument,
    for the given hero. It takes a list of potential_items (a list of Dota2Item objects) and a hero (a PlayerHero object)
    as input parameters and returns a boolean value indicating if the purchase was successful or not.
    """
    affordable_items = get_affordable_items(hero, item_list)
    courier = get_courier(hero, world)
    if affordable_items:
        max_score_item = max(affordable_items,
                             key=lambda item: calculate_item_score(hero, item, role, attributes, world))
        if max_score_item is not None and not hero_has_item(hero, max_score_item) and not courier_has_item(hero,
                                                                                                           max_score_item,
                                                                                                           world):
            print("MAX SCORE AFFORDABLE ITEM = " + max_score_item.name)
            if isinstance(max_score_item, RecipeItem):
                if is_item_secret_shop(max_score_item):
                    if courier.is_in_range_of_secret_shop():
                        hero.buy_combined(generate_item_components_list(max_score_item, get_all_the_items(hero, world)))
                        return True
                    else:
                        courier_to_secret_shop(hero, world)
                        return True
                else:
                    print("BUYING RECIPE ITEM")
                    hero.buy_combined(generate_item_components_list(max_score_item, get_all_the_items(hero, world)))
                    return True
            else:
                if max_score_item.secret_shop:
                    if courier.is_in_range_of_secret_shop():
                        hero.buy(max_score_item.name)
                        return True
                    else:
                        courier_to_secret_shop(hero, world)
                        return True
                else:
                    print("BUYING NON-RECIPE ITEM")
                    hero.buy(max_score_item.name)
                return True
        print("MAX SCORE ITEM IS NONE OR HERO ALREADY AHS THE ITEM")
    print("RETURNING FALSE")
    return False


def calculate_item_score(hero: PlayerHero, item: Dota2Item, role: Dota2Role, attribute: list[Dota2Attribute],
                         world: World) -> float:
    """
    hero (PlayerHero): The hero who's doing the purchasing
    item (Dota2Item): The item that the hero wishes to purchase
    role (Dota2Role): The role of the hero
    attribute (Dota2Attribute): The attributes that the hero wishes to prioritize
    """
    if role == Dota2Role.CARRY:
        return calculate_carry_item_score(hero, item, attribute, world)
    elif role == Dota2Role.SUPPORT:
        return calculate_support_item_score(hero, item, attribute, world)
    elif role == Dota2Role.UTILITY:
        return calculate_utility_item_score(hero, item, attribute, world)
    return 0


def calculate_carry_item_score(hero: PlayerHero, item: Dota2Item, attribute: list[Dota2Attribute],
                               world: World) -> float:
    """
    hero (PlayerHero): The hero who's doing the purchasing
    item (Dota2Item): The item that the hero wishes to purchase
    attribute (Dota2Attribute): The attribute that the hero wishes to prioritize
    """
    score = 1
    bonus_damage_weight = 2.0
    print("BEGIN: " + item.name)
    pprint(item.attribute)
    if hero_has_item(hero, item) or courier_has_item(hero, item, world):
        print("hero already has this item, skipping", item.name)
        return 0

    # Add 2 points for every point of the desired attribute
    for attribute in attribute:
        if str(attribute.value) in item.attribute.keys():
            score += float(item.attribute[str(attribute.value)]) * 2

    # Add 2 points for every bonus damage point
    if "bonus_damage" in item.attribute.keys():
        score += bonus_damage_weight
        print("----bonus_damage " + str(score))

    # Add 1 point for every 10 attack speed points
    if "bonus_attack_speed" in item.attribute.keys():
        score += float(item.attribute["bonus_attack_speed"]) // 10
        print("----bonus_attack_speed " + str(score))

    # Add 1 point for every 3% lifesteal
    if "lifesteal_percent" in item.attribute.keys():
        score += float(item.attribute["lifesteal_percent"]) // 3
        print("----lifesteal_percent " + str(score))

    # Add 1 point for every 3 points of armor
    if "bonus_armor" in item.attribute.keys():
        score += float(item.attribute["bonus_armor"]) // 3
        print("----bonus_armor " + str(score))
    print(item.name + ", score: " + str(score))
    print("END\n")
    return score


def calculate_support_item_score(hero: PlayerHero, item: Dota2Item, attribute: list[Dota2Attribute],
                               world: World) -> float:
    """
        hero (PlayerHero): The hero who's doing the purchasing
        item (Dota2Item): The item that the hero wishes to purchase
        attribute (Dota2Attribute): The attribute that the hero wishes to prioritize
        """
    score = 1
    bonus_damage_weight = 2.0
    print("BEGIN: " + item.name)
    pprint(item.attribute)
    if hero_has_item(hero, item) or courier_has_item(hero, item, world):
        print("hero already has this item, skipping", item.name)
        return 0

    # Add 2 points for every point of the desired attribute
    for attribute in attribute:
        if str(attribute.value) in item.attribute.keys():
            score += float(item.attribute[str(attribute.value)]) * 2

    if "bonus_all_stats" in item.attribute.keys():
        score += float(item.attribute["bonus_all_stats"]) * 2
        print("----bonus_all_stats " + str(score))

    if "health_regen" in item.attribute.keys():
        score += float(item.attribute["health_regen"])
        print("----health_regen " + str(score))

    if "mana_regen" in item.attribute.keys():
        score += float(item.attribute["mana_regen"])
        print("----mana_regen " + str(score))

    # Add 0.1 points for every range point
    if "bonus_cast_range" in item.attribute.keys():
        score += float(item.attribute["bonus_cast_range"]) * 0.1
        print("----bonus_damage " + str(score))

     # Add 0.1 points for every range point
    if "armor" in item.attribute.keys():
        score += float(item.attribute["armor"]) * 1
        print("----armor " + str(score))

    # Add 1 point for every mana regen point
    if "bonus_mana_regen" in item.attribute.keys():
        score += float(item.attribute["bonus_mana_regen"])
        print("----bonus_attack_speed " + str(score))

    # Add 1 point for every 2% magic resistance
    if "bonus_magic_resistance" in item.attribute.keys():
        score += float(item.attribute["bonus_magic_resistance"]) // 2
        print("----magic_resistance" + str(score))

    # Add 1 point for every 3 points of armor
    if "bonus_armor" in item.attribute.keys():
        score += float(item.attribute["bonus_armor"]) // 3
        print("----bonus_armor " + str(score))
    print(item.name + ", score: " + str(score))
    print("END\n")
    return score


def calculate_utility_item_score(hero: PlayerHero, item: Dota2Item, attribute: list[Dota2Attribute],
                               world: World) -> float:
    """
        hero (PlayerHero): The hero who's doing the purchasing
        item (Dota2Item): The item that the hero wishes to purchase
        attribute (Dota2Attribute): The attribute that the hero wishes to prioritize
    """
    score = 1
    bonus_damage_weight = 2.0
    print("BEGIN: " + item.name)
    pprint(item.attribute)
    if hero_has_item(hero, item) or courier_has_item(hero, item, world):
        print("hero already has this item, skipping", item.name)
        return 0

    # Add 2 points for every point of the desired attribute
    for attribute in attribute:
        if str(attribute.value) in item.attribute.keys():
            score += float(item.attribute[str(attribute.value)]) * 2

    if "bonus_all_stats" in item.attribute.keys():
        score += float(item.attribute["bonus_all_stats"]) * 2
        print("----bonus_all_stats " + str(score))

    # Add 0.1 points for every range point
    if "bonus_armor" in item.attribute.keys():
        score += float(item.attribute["bonus_armor"])
        print("----bonus_armor " + str(score))

    if "armor" in item.attribute.keys():
        score += float(item.attribute["armor"]) * 2
        print("----armor " + str(score))

    if "health_regen" in item.attribute.keys():
        score += float(item.attribute["health_regen"]) * 2
        print("----health_regen " + str(score))

    # Add 1 point for every mana regen point
    if "bonus_health_regen" in item.attribute.keys():
        score += float(item.attribute["bonus_health_regen"])
        print("----bonus_health_regen " + str(score))

    # Add 1 point for every 2% magic resistance
    if "bonus_health" in item.attribute.keys():
        score += float(item.attribute["bonus_health"]) // 10
        print("----bonus_health " + str(score))

    # Add 1 point for every 3 points of armor
    if "bonus_magic_resistance" in item.attribute.keys():
        score += float(item.attribute["bonus_magic_resistance"]) // 3
        print("----bonus_magic_resistance " + str(score))
    print(item.name + ", score: " + str(score))
    print("END\n")
    return score
