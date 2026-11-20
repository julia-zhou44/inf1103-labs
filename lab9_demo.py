# testing to verify predication (5.1)

from file_handling import load_products
from inventory import Inventory
from main import get_positive_float
from supplier import Supplier


def demo_input_helper() -> None:
    print("\n=== 5.1 get_positive_float: try abc, then -5, then 12.50 ===")
    value = get_positive_float("Price: ")
    print("Returned:", value)


def demo_load_products() -> None:
    print("\n=== 5.2 load_products(products.csv) ===")
    supplier = Supplier("S000", "Default Supplier", "-")
    inventory = Inventory()
    load_products("products.csv", inventory, supplier)
    inventory.display_all_products()

    print("\n=== 5.2 load_products with a missing file ===")
    load_products("missing_products.csv", Inventory(), supplier)


if __name__ == "__main__":
    demo_input_helper()
    demo_load_products()