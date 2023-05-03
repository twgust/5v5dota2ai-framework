from abc import abstractmethod
from ctypes import Union

from bots.test_bots.design.abstraction.Dota2Item import Dota2Item
from bots.test_bots.design.abstraction.RecipeItem import RecipeItem


class Role:
    item_blacklist = [
        "tango_single",
    ]

    # works
    def find_items_by_cost(self, gold: int, items: list[Dota2Item]) -> list[Dota2Item]:
        # Sort the items list based on cost using a lambda function
        # self.validate_list_of_items(items)
        items.sort(key=lambda item: item.cost)
        copy = items.copy()
        for item in items:
            if isinstance(item, RecipeItem) or "recipe" in item.name or item.cost == 0:
                print("ignore")
            for blacklisted_item in self.item_blacklist:
                if blacklisted_item in item.name:
                    print("ignore")

        # Perform binary search to find the first index i such that items[i].cost < gold
        lo, hi = 0, len(copy) - 1
        while lo <= hi:
            mid = (lo + hi) // 2
            if copy[mid].cost <= gold:
                lo = mid + 1
            else:
                hi = mid - 1

        # Return the items whose cost is less than or equal to gold
        my_items = copy[:lo]
        return my_items

    def validate_list_of_items(self, items: list[Dota2Item]) -> list[Dota2Item]:
        print("VALIDATE LIST OF ITEMS")

        return items

    @abstractmethod
    def get_best_items(self, role_name: str, attribute: str) -> dict[str, int]:
        pass

    @abstractmethod
    def buy_items(self, role_name: str) -> list[Dota2Item]:
        pass
