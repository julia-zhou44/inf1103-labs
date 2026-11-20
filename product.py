# product.py

from abc import ABC, abstractmethod
from supplier import Supplier


class Product(ABC):

    def __init__(self, product_id: str, name: str, price: float, stock: int, supplier: Supplier):
        # validation: Product owns these rules, so every subclass gets them automatically
        if not isinstance(price, (int, float)) or price <= 0:
            raise ValueError("Price must be a number greater than zero.")
        self._validate_stock(stock)

        self.__product_id: str = product_id
        self.__name: str = name
        self.__price: float = price
        self.__stock: int = stock
        self.__supplier: Supplier = supplier

    # getters: let outside code READ the data without changing it

    def get_product_id(self) -> str:
        return self.__product_id

    def get_name(self) -> str:
        return self.__name

    def get_price(self) -> float:
        return self.__price

    def get_stock(self) -> int:
        return self.__stock

    def get_supplier(self) -> Supplier:
        return self.__supplier


    @staticmethod
    def _validate_stock(quantity: int) -> None:
        """Shared stock rule, used by __init__ and update_stock. Raises ValueError if broken."""
        if not isinstance(quantity, int) or quantity < 0:
            raise ValueError("Stock quantity must be a whole number (0 or more).")

    def update_stock(self, quantity: int) -> None:
        """Replace the stock. Raises ValueError if the quantity is invalid."""
        self._validate_stock(quantity)
        self.__stock = quantity

    def display_information(self) -> None:
        print(f"ID: {self.__product_id} | Name: {self.__name} | "
              f"Price: ${self.__price:.2f} | Stock: {self.__stock}")
        print(f"    Supplier: {self.__supplier.get_name()}")

    def to_dict(self) -> dict:
        """Turn this product into a dictionary (used when saving to json)"""
        return {"id": self.__product_id, "name": self.__name,
                "price": self.__price, "stock": self.__stock,
                "supplier": self.__supplier.to_dict()}

    
    @abstractmethod
    def get_fulfilment_info(self) -> str:
        """Return delivery/fulfilment information for this product type"""