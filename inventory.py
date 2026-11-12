# inventory.py

LINE = "-" * 45

class Inventory: # Manages a collection of Product object

    def __init__(self):
        self.__products = []  # list of Product objects

    def add_product(self, product):
        """Add a product. Return False if the ID already exists."""
        if self.search_product(product.get_product_id()) is not None:
            return False
        self.__products.append(product)
        return True

    def search_product(self, product_id):
        """Return the Product with this ID, or None."""
        for product in self.__products:
            if product.get_product_id() == product_id:
                return product
        return None

    def display_all(self):
        print("\nCurrent Inventory")
        print(LINE)
        if not self.__products:
            print("(no products in inventory)")
        for product in self.__products:
            product.display_information()
            print()
        print(LINE)

    def get_products(self):
        """Return a copy of the product list (so outside code can't change the real one)."""
        return list(self.__products)