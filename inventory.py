# inventory.py

from product import Product

LINE = "-" * 45

class Inventory: # aggregation: groups Product objects but does not create or own them

    def __init__(self) -> None:
        self.__products: list[Product] = []  # list of Product objects

    def add_product(self, product: Product) -> bool:
        """Add a product. Return False if the ID already exists."""
        if self.find_product(product.get_product_id()) is not None:
            return False
        self.__products.append(product)
        return True

    def remove_product(self, product_id: str) -> bool:
        """Remove a product by its ID. Return True if successful, False otherwise."""
        product = self.find_product(product_id)
        if product:
            self.__products.remove(product)
            return True
        return False

    def find_product(self, product_id: str) -> Product | None:
        """Return the Product with this ID, or None."""
        for product in self.__products:
            if product.get_product_id() == product_id:
                return product
        return None

    def display_all_products(self) -> None:
        print("\nCurrent Inventory")
        print(LINE)
        if not self.__products:
            print("(no products in inventory)")
        for product in self.__products:
            product.display_information()  # polymorphism: each object runs its own version
            print()
        print(LINE)

    def get_products(self) -> list[Product]:
        """Return a copy of the product list (so outside code can't change the real one)."""
        return list(self.__products)