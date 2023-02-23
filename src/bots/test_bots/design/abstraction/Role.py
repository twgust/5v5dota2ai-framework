from abc import abstractmethod


class Role():

    @abstractmethod
    def get_best_items(self, role_name: str, attribute: str) -> dict[str, int]:
        pass

