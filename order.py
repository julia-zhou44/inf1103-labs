# order.py

from product import Product


class OrderLine:
    """One product + quantity inside an Order. Only Order should create these (composition)"""

    def __init__(self, product: Product, quantity: int) -> None:
        self.__product: Product = product      # association: refers to the Product, does not own it
        self.__quantity: int = quantity

    def get_product(self) -> Product:
        return self.__product

    def get_quantity(self) -> int:
        return self.__quantity

    def calculate_subtotal(self) -> float:
        return self.__product.get_price() * self.__quantity

    def display_information(self) -> None:
        print(f"{self.__product.get_name()} x {self.__quantity} = "
              f"${self.calculate_subtotal():.2f}")


class Order:
    """Composition: an Order creates, owns and removes its own OrderLine objects """

    def __init__(self, order_id: str) -> None:
        self.__order_id: str = order_id
        self.__order_lines: list[OrderLine] = []

    def get_order_id(self) -> str:
        return self.__order_id

    def add_order_line(self, product: Product, quantity: int) -> None:
        order_line = OrderLine(product, quantity)   # the Order creates the part itself
        self.__order_lines.append(order_line)

    def remove_order_line(self, product_id: str) -> bool:
        """Remove the line for this product. Return False if no such line"""

        for line in self.__order_lines:

            if line.get_product().get_product_id() == product_id:
                self.__order_lines.remove(line)
                return True
            
        return False

    def get_order_lines(self) -> list[OrderLine]:
        """Return a copy so outside code can't add/move lines directly"""
        return list(self.__order_lines)

    def calculate_total(self) -> float:
        return sum(line.calculate_subtotal() for line in self.__order_lines)

    def display_order(self) -> None:
        print(f"\nOrder {self.__order_id}")
        
        for line in self.__order_lines:
            line.display_information()
        print(f"Total: ${self.calculate_total():.2f}")