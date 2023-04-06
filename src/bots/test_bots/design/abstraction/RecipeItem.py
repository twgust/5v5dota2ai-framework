from bots.test_bots.design.abstraction.Dota2Item import Dota2Item


# # entity class which represents a recipe item, this is a special type of item which requires many smaller items to
# be crafted # this class is a child of the Dota2Item class, it also has a list of items which are required to craft
# it # this class is used to represent the recipe items in the game

class RecipeItem(Dota2Item):
    def __init__(self, name: str, cost: int, is_active: bool, notes: str, attribute: str,
                 required_items: list[Dota2Item]):
        super().__init__(name, cost, is_active, notes, attribute)
        self.required_items = required_items

    def get_required_items(self) -> list[Dota2Item]:
        return self.required_items

    def to_string(self) -> str:
        return self.name
