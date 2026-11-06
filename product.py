# product.py

from abc import ABC, abstractmethod

class Product(ABC):
    
    def __init__(self, product_id, name, price, stock):
        self.__product_id = product_id
        self.__name = name
        self.__price = price
        self.__stock = stock

    # getters: let outside code READ the data without changing it
    def get_product_id(self):
        return self.__product_id

    def get_name(self):
        return self.__name

    def get_price(self):
        return self.__price

    def get_stock(self):
        return self.__stock

    def update_stock(self, quantity):
        """Replace the stock. Return True if accepted, False if invalid."""
        if not isinstance(quantity, int) or quantity < 0:
            return False
        self.__stock = quantity
        return True

    def display_information(self):
        print(f"ID: {self.__product_id} | Name: {self.__name} | "
              f"Price: ${self.__price:.2f} | Stock: {self.__stock}")

    def to_dict(self):
        """Turn this product into a dictionary (used when saving to JSON)."""
        return {"id": self.__product_id, "name": self.__name,
                "price": self.__price, "stock": self.__stock}


    @abstractmethod
    def get_fulfilment_info(self) -> str:
        """Return delivery/fulfilment information for this product type."""