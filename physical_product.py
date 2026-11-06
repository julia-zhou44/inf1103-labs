# physical_product.py
from product import Product
from CanBeShipped import CanBeShipped


class PhysicalProduct(Product, CanBeShipped):
    def __init__(self, product_id, name, price, stock, weight):
        super().__init__(product_id, name, price, stock)   # reuse parent constructor
        self.__weight = weight                             # in kg

    def get_weight(self):
        return self.__weight

    def display_information(self):
        super().display_information()                      # parent prints the common line
        print(f"    Type: Physical | Weight: {self.__weight} kg")

    def calculate_shipping_cost(self) -> float:
        return round(5.00 + 2.00 * self.__weight, 2)       # $5 base + $2 per kg

    def get_fulfilment_info(self) -> str:
        return "Requires physical shipping."

    def to_dict(self):
        """Add the type and weight to the parent's dictionary (used when saving to JSON)."""
        data = super().to_dict()                           # id, name, price, stock from the parent
        data["type"] = "physical"
        data["weight"] = self.__weight
        return data