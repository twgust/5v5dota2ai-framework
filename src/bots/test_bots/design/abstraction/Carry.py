from bots.test_bots.design.abstraction.Role import Role

# implementation of a hero, e.g. __init__(self, 'sniper', 'strength')
class Carry(Role):
    def __init__(self, hero_name, attribute):
        self.hero_name = hero_name
        self.attribute = attribute
        print("INIT CARRY")
        best_carry_items_dict = self.get_best_items("carry", "intelligence")

    def get_attribute(self):
        return self.attribute

    def get_hero_name(self):
        return self.hero_name

    def get_best_items(self, role: str, attribute: str) -> dict[str, int]:
        print("ok")