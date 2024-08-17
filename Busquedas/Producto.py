class Producto:
    def __init__(self, id: str, name: str, price: float, description: str):
        self._id = id
        self._name = name
        self._price = price
        self._description = description

    # Getters
    def get_id(self) -> str:
        return self._id

    def get_name(self) -> str:
        return self._name

    def get_price(self) -> float:
        return self._price

    def get_description(self) -> str:
        return self._description

    # Setters
    def set_id(self, id: str):
        self._id = id

    def set_name(self, name: str):
        self._name = name

    def set_price(self, price: float):
        self._price = price

    def set_description(self, description: str):
        self._description = description