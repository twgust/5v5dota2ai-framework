from typing import List, Type, Any

from bots.test_bots.design.abstraction.Dota2Item import Dota2Item
from bots.test_bots.design.abstraction.RecipeItem import RecipeItem
from bots.test_bots.design.abstraction.Role import Role
from game.player_hero import PlayerHero
from bots.test_bots.design.abstraction.ItemsList import ItemsList


# implementation of a hero, e.g. __init__(self, 'sniper', 'strength')
class Carry(Role):
    # OFF == Only buy items in _target_items,
    # ON == Buy items in _target_items and items that are good for the hero
    _smart_buy = False
    _attribute: str
    _my_items_list: ItemsList
    _target_items: [Dota2Item]
    _shopping_list: [Dota2Item]

    def __init__(self, hero: PlayerHero, attribute: str):
        self.player_hero = hero
        self._attribute = attribute
        self._my_items_list = ItemsList()
        self._target_items = [Dota2Item("tango", 90, True, "item_description", None)]
        self._shopping_list = []
        print("INIT CARRY")

    def get_attribute(self):
        return self._attribute

    def get_hero_name(self):
        return self.player_hero.get_name()

    def validate_list_of_items(self, items: list[Dota2Item]) -> list[Dota2Item]:
        current_items = self.player_hero.get_items()
        items = [item for item in items if item.name not in [current_item.name for current_item in current_items]]
        return items

    def attempt_item_purchase(self, item: Dota2Item) -> bool:
        """
        Attempts to purchase a single item.
        Parameters:
        item (Dota2Item): The item to be purchased.
        Returns:
        bool: True if the purchase was successful, False otherwise.
        """
        if self.player_hero.get_gold() > item.cost:
            self.player_hero.buy(item.name)
            return True
        else:
            # item is too expensive so we return false
            return False


    def attempt_partial_item_purchase(self, item: RecipeItem) -> bool:
        """
        Attempts to purchase a partial item using its recipe.
        Parameters:
        item (RecipeItem): The recipe of the item to be purchased.
        Returns:
        bool: True if the purchase was successful, False otherwise.
        """
        for component in item.get_required_items():
            if component.name not in [item.name for item in self.player_hero.get_items()]:
                if self.attempt_item_purchase(component):
                    return True
        return False

    def attempt_complete_item_purchase(self, item: RecipeItem) -> bool:
        """
        Attempts to purchase a complete item using its recipe.
        Parameters:
        item (RecipeItem): The recipe of the item to be purchased.
        Returns:
        bool: True if the purchase was successful, False otherwise.
        """
        components = self.generate_item_tuple(item)
        if self.player_hero.get_gold() > item.cost:
            self.player_hero.buy_combined(list(components))
            return True
        else:
            return False

    def generate_item_tuple(self, item: RecipeItem) -> tuple:
        components = item.get_required_items()
        item_names_tuple = tuple(component.name for component in components)
        return item_names_tuple

    def buy_recipe_item(self, item: RecipeItem) -> bool:
        """
        This function attempts to buy a recipe item by first checking if the player can afford to buy the complete item
        using `attempt_complete_item_purchase`, and if not, it attempts to buy the item's required components using
        `attempt_partial_item_purchase`. If the purchase is successful, it returns `True`, else it returns `False`.

        :param item: A `RecipeItem` object representing the item to be purchased.
        :return: A boolean value indicating whether the purchase was successful.
        """
        # components = item.get_required_items()
        buy_status = self.attempt_complete_item_purchase(item)
        if not buy_status:
            return self.attempt_partial_item_purchase(item)
        elif buy_status:
            return buy_status

    def debug_buying(self, item: Dota2Item, function_name: str):
        print(
            self.player_hero.get_name() + "--DEBUG: invoking -> " + function_name + "() " + item.get_name() + " " + str(
                item.cost))

    def buy_target_items(self) -> list[Dota2Item]:
        bought_items = []
        for target_item in self._target_items:
            if target_item.cost < self.player_hero.get_gold():
                buy_item = "item_" + target_item.name
                self.player_hero.buy(buy_item)
                self._target_items.remove(target_item)
                bought_items.append(target_item)
        return bought_items

    # WIP

    # WIP
    def buy_max_cost_item(self, potential_items: list[Dota2Item]) -> Dota2Item:
        if potential_items:
            # buy the item with the highest cost affordable to hero
            max_cost_item = max(potential_items, key=lambda item: item.cost)
            buy_item = "item_" + max_cost_item.get_name()
            self.player_hero.buy(buy_item)
            return max_cost_item

    #WIP
    def buy_items(self, role_name: str) -> Any | None:
        # start gold
        print(self.player_hero.get_name() + " INVENTORY: " + " ,".join(
            [str(x.get_name()) for x in self.player_hero.get_items()]))
        recipe_item = self._my_items_list.get_recipe_item_dict().get("item_bracer")
        print(recipe_item.get_required_items())
        #for s in recipe_item.get_required_items():
           # print(s)
        # self.generate_item_tuple(recipe_item)   #TEST
        if self.buy_recipe_item(recipe_item):  # Test
            print("BUY_RECIPE_ITEM returns true")
            return True
        else:
            print("BUY_RECIPE_ITEM returns false")
            return False

        # get items for the attribute we're focusing on building for
        items_attribute_list = self._my_items_list.get_attribute_list(self.get_attribute())
        # smart_buy is ON
        if self._smart_buy:
            # first priority is buying items in target list
            # self.buy_target_items()
            # second priority is buying items that are potentially good for the hero

            # get potential items, based on hero gold and attribute
            potential_items = self.find_items_by_cost(self.player_hero.get_gold(), items_attribute_list)
            # buy the most expensive item in the list
            bought_item = self.buy_max_cost_item(potential_items)
            # add bought item to shopping list
            self._shopping_list.append(bought_item)
            # return the shopping list
            return self._shopping_list
        # smart_buy is OFF
        else:
            ##self._shopping_list.append(self.buy_target_items())
            return self._shopping_list

    def get_best_items(self, role_name: str, attribute: str) -> dict[str, int]:
        pass
