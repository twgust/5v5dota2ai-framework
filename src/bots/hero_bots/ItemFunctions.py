from bots.test_bots.design.abstraction.Dota2Item import Dota2Item
from bots.test_bots.design.abstraction.RecipeItem import RecipeItem
from game.player_hero import PlayerHero


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
        max_cost_item = max(potential_items, key=lambda item: item.cost if item.cost <= hero.get_gold() else float('-inf'))
        if max_cost_item is not None:
            if max_cost_item.name not in [item.name for item in hero.get_items()]:
                if isinstance(max_cost_item, RecipeItem):
                    hero.buy_combined(list(generate_item_tuple(max_cost_item)))
                else:
                    hero.buy(max_cost_item.name)
                return True
    return False
