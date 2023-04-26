## data structure for the class Dota2Item.py, represents a list of items. Initializes the list by using OpenDota2API.py to get the list of items from OpenDota2 API
from bots.test_bots.design.abstraction.Dota2Item import Dota2Item
import json
import ijson
from bots.test_bots.design.abstraction.RecipeItem import RecipeItem


class ItemsList:
    _items_list: list[Dota2Item]
    _items_list_passive: list[Dota2Item]
    _items_list_active: list[Dota2Item]

    _items_list_strength: list[Dota2Item]
    _items_list_agility: list[Dota2Item]
    _items_list_intelligence: list[Dota2Item]

    _items_list_recipes: list[RecipeItem]

    def __init__(self):
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
            if not item.hasActiveEffect:
                passive_items_list.append(item)
        return passive_items_list

    def getAllActiveItems(self) -> list[Dota2Item]:
        active_items_list = []
        for item in self._items_list:
            if item.hasActiveEffect:
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

    def jsonOpener(self, filename: str) -> list:
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
                if item_components is None:
                    dota2_item = Dota2Item(name, item_cost, item_has_active_effect, item_notes, attrib_array)
                    self.validateDota2Item(dota2_item)
                    # can probably remove this
                    if item_cost != 0:
                        itemlist.append(dota2_item)
                else:
                    dota2_item = RecipeItem(name, item_cost, item_has_active_effect, item_notes, attrib_array,
                                            item_components)
                    self.validateDota2Item(dota2_item)
                    # can probably remove this
                    if item_cost != 0:
                        itemlist.append(dota2_item)

                i = i + 1
        print("Finished Reading JSON file which contains multiple JSON document")
        return itemlist

    @property
    def items_list_strength(self):
        return self._items_list_strength
