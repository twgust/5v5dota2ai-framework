## data structure for the class Dota2Item.py, represents a list of items. Initializes the list by using OpenDota2API.py to get the list of items from OpenDota2 API
from bots.test_bots.design.abstraction.Dota2Item import Dota2Item
import json
import ijson
from bots.test_bots.design.abstraction.RecipeItem import RecipeItem


class ItemsList:
    _items_list: list[Dota2Item]

    _items_dict: dict[str, Dota2Item]

    # K = item.name, V = recipeItem
    _items_dict_recipe: dict[str, RecipeItem]

    _items_list_passive: list[Dota2Item]
    _items_list_active: list[Dota2Item]

    _items_list_strength: list[Dota2Item]
    _items_list_agility: list[Dota2Item]
    _items_list_intelligence: list[Dota2Item]

    _items_list_recipes: list[RecipeItem]

    def __init__(self):
        self._items_dict = {}
        self._items_dict_recipe = {}
        self.load_data()
        print("Ok")

    def load_data(self):
        self._items_list = self.jsonOpener('bots/test_bots/design/abstraction/items.json')
        self._items_list.sort(key=lambda item: item.cost)
        self._items_list_passive = self.getAllPassiveItems()
        self._items_list_active = self.getAllActiveItems()
        self._items_list_recipes = self.getAllRecipeItems()
        self.generate_attribute_lists()

        # self.openJsonFile('items.json')
        # self.items_list = self.openJsonFile('items.json')
        #  for item in self.items_list:
        #     print(item)
        # print("--------------------\n\n")
        # self.parse_items_list(dict)
        print("test")

    def get_attribute_list(self, attribute: str) -> list[Dota2Item]:
        if attribute == "Strength":
            return self._items_list_strength
        elif attribute == "Agility":
            return self._items_list_agility
        elif attribute == "Intelligence":
            return self._items_list_intelligence
        else:
            return self.get_items_list()

    def get_items_list(self) -> list[Dota2Item]:
        return self._items_list

    def parse_items_list(self, json: dict) -> list[Dota2Item]:
        for item in json:
            print(item)
            if item["cd"] <= 0:
                dota2_item = Dota2Item(item["dname"], item["cost"], False, item["notes"], item["attribute"])
            else:
                dota2_item = Dota2Item(item["dname"], item["cost"], True, item["notes"], item["attribute"])
            self.items_list.append(dota2_item)
        return self.items_list

    # file is too large and can't be read in one go so we need to read it in chunks and then parse it into a json object
    def openJsonFile(self, filename: str) -> list:
        with open(filename, 'r') as file:
            parser = ijson.parse(file)
            data = []
            i = 0
            for prefix, event, value in parser:
                if '.' not in prefix:
                    print(str(prefix) + " PREFIX " + str(i))
                    print(str(event) + " EVENT" + str(i))
                    print(str(value) + " VALUE" + str(i))
                    i = i + 1
            # print(value)
        return data

    def generate_attribute_lists(self) -> None:
        strength_items_list = []
        intelligence_items_list = []
        agility_items_list = []
        for item in self._items_list:
            for attribute in item.attribute:
                if attribute == "Strength":
                    strength_items_list.append(item)
                elif attribute == "Intelligence":
                    intelligence_items_list.append(item)
                elif attribute == "Agility":
                    agility_items_list.append(item)
        self._items_list_strength = strength_items_list
        self._items_list_agility = agility_items_list
        self._items_list_intelligence = intelligence_items_list

    def getAllPassiveItems(self) -> list[Dota2Item]:
        passive_items_list = []
        for item in self._items_list:
            if not item.has_active_effect():
                passive_items_list.append(item)
        return passive_items_list

    def get_item_dict(self) -> dict[str, Dota2Item]:
        return self._items_dict

    def get_recipe_item_dict(self) -> dict[str, RecipeItem]:
        return self._items_dict_recipe

    def getAllActiveItems(self) -> list[Dota2Item]:
        active_items_list = []
        for item in self._items_list:
            if item.get_active_effect():
                active_items_list.append(item)
        return active_items_list

    def getAllRecipeItems(self) -> list[RecipeItem]:
        recipe_items_list = []
        for item in self._items_list:
            if isinstance(item, RecipeItem):
                recipe_items_list.append(item)
        return recipe_items_list

    def validateDota2Item(self, item: Dota2Item) -> Dota2Item:
        if item.cost is None:
            item.cost = 0
            return item

    def createRecipeItem(self, item: str, data: dict) -> RecipeItem:
        """
        This function attempts to create a RecipeItem object from the given item name and data dictionary. If the
        item is a recipe, it creates a RecipeItem object and returns it. If the item is not a recipe, it returns
        None.
        :param item: The name of the item to be created :param data: The data dictionary to be used to create
        the item
        :param data: The data dictionary to be used to create the item
        :return: The created RecipeItem object or None
        """
        item_components = data.get(item).get("components")
        print(item_components)
        item_cd = data.get(item).get("cd")
        required_items_list = []
        print("item: " + item)
        for component in item_components:
            if component is not None or component != "":
                print("component: " + component)
                temp_dota2_item_name = "item_" + component
                temp_dota2_item_cost = data.get(component).get("cost")
                if int(item_cd) <= 0:
                    temp_dota2_item_active_effect = False
                else:
                    temp_dota2_item_active_effect = True
                temp_dota2_item_notes = data.get(component).get("hint")
                temp_dota2_item_attribs = data.get(component).get("attrib")
                dota2_item = Dota2Item(temp_dota2_item_name, temp_dota2_item_cost, temp_dota2_item_active_effect,
                                       temp_dota2_item_notes, temp_dota2_item_attribs)
                required_items_list.append(dota2_item)

        recipe = self.find_recipe_for_item(item, data)
        if recipe is not None:
            required_items_list.append(recipe)
        recipe_item = RecipeItem(str("item_" + item), data.get(item).get("cost"), False,
                                 data.get(item).get("hint"), data.get(item).get("attrib"), required_items_list)
        return recipe_item

    def find_recipe_for_item(self, item: str, data: dict) -> Dota2Item | None:
        """
        This function searches for a recipe of a given item within the data dictionary. If it
        finds one, it returns the recipe as a dota 2 item. If it does not find one, it returns None.
        Necessary because recipe_bracer is not in the components list of bracer in items.json...
        """
        recipe_item = None
        for json_item in data.keys():
            if json_item == "recipe_" + item:
                return Dota2Item(str("item_recipe_" + item), data.get(json_item).get("cost"), False, None, None)
        return None

        # returns false if the item is a component of another item

    # returns true if the item is not a component of another item
    def isBaseItem(self, item: str, data: dict) -> bool:
        """
        This function checks if the given item is a component of another item. If it is, it returns false. If it is
        not, it returns true.
        """
        item_list = data.keys()
        # iterate over all the entries in the json file
        for json_item in item_list:
            # if the components of an entry isn't null
            if data.get(json_item).get("components") is not None:
                # if list of components contains our item return false
                if data.get(json_item).get("components").__contains__(item):
                    print("original item [" + item + "] is a component of another item [" + json_item + "] "
                          + "with components: " + str(data.get(json_item).get("components")))
                    return False
        return True

    def jsonOpener(self, filename: str) -> list:
        """
        This function opens a json file of dota 2 items and returns a list of the items in the file.
        :param filename: The name of the file to be opened
        :return: A list of the items in the file
        """
        itemlist = []
        print("Started Reading JSON file which contains multiple JSON document")
        with open(filename, 'r') as f:
            data = json.load(f)
            list_of_items = data.keys()
            myList = list(list_of_items)
            item_has_active_effect = False
            i: int = 0
            for item in list_of_items:
                name = myList.__getitem__(i)
                name = "item_" + name
                item_name = data.get(item).get("dname")
                item_cd = data.get(item).get("cd")
                item_notes = data.get(item).get("notes")
                if int(item_cd) <= 0:
                    item_has_active_effect = False
                else:
                    item_has_active_effect = True
                item_components = data.get(item).get("components")
                item_cost = data.get(item).get("cost")
                attribs = data.get(item).get("attrib")
                if attribs is None:
                    item_attribute = "None"
                    # print(item_attribute)
                else:
                    attrib_array = []
                    for attrib in attribs:
                        # print(attrib.keys())
                        # print(attrib.values())
                        item_attribute = attrib.get("header")
                        # print(item_attribute)
                        if attrib.get("header") == "+" or attrib.get("header") == "-":
                            attribute_value = attrib.get("value")
                            attrib_array.append(attrib.get("footer"))
                            # attribute_footer = attrib.get("footer")
                        else:
                            attribute_value = "empty"
                            attrib_array.append(attribute_value)

                # check to see if item is a base item,
                # if it is, create a Dota2Item object,
                # if not, create a RecipeItem object
                if self.isBaseItem(item, data):
                    dota2_item = Dota2Item(name, item_cost, item_has_active_effect, item_notes, attrib_array)
                    self.validateDota2Item(dota2_item)
                    itemlist.append(dota2_item)
                    self.add_to_dictionary(dota2_item)

                if item_components is not None:
                    recipe_item = self.createRecipeItem(item, data)
                    if recipe_item is not None:
                        self.validateDota2Item(recipe_item)
                        itemlist.append(self.createRecipeItem(item, data))
                        self.add_to_dictionary(recipe_item)
                        self._items_dict_recipe[recipe_item.name] = recipe_item
                i = i + 1
        print("Finished Reading JSON file which contains multiple JSON document")
        return itemlist

    def add_to_dictionary(self, item: Dota2Item):
        self._items_dict[item.name] = item

    @property
    def items_list_strength(self):
        return self._items_list_strength
