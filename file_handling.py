# file_handling.py
import json
import os

from inventory import Inventory
from product_factory import ProductFactory
from supplier import Supplier

DATA_DIR = "data"
DATA_FILE = os.path.join(DATA_DIR, "inventory.json")

# used for old products in inventory.json that were saved before suppliers existed
DEFAULT_SUPPLIER = Supplier("S000", "Unknown Supplier", "-")

def get_supplier(item: dict, suppliers: dict[str, Supplier]) -> Supplier:
    """Return the Supplier for this product, reusing the same object if the ID was already seen."""
    data = item.get("supplier")
    
    if data is None:
        return DEFAULT_SUPPLIER
    supplier_id = data["supplier_id"]
    
    if supplier_id not in suppliers:
        suppliers[supplier_id] = Supplier(supplier_id, data["name"], data["contact_email"])
    return suppliers[supplier_id]

def load_inventory() -> Inventory:
    """Read inventory.json and return a filled Inventory object"""

    inventory = Inventory()
    suppliers: dict[str, Supplier] = {}   # products from the same supplier share ONE Supplier object

    if not os.path.exists(DATA_FILE):
        print("inventory.json not found. Starting with an empty inventory.")
        return inventory

    try:
        with open(DATA_FILE, "r") as file:
            data = json.load(file)

    except (json.JSONDecodeError, OSError):
        print("inventory.json is unreadable. Starting with an empty inventory.")
        return inventory

    if not isinstance(data, list):
        print("inventory.json has the wrong format. Starting with an empty inventory.")
        return inventory

    for item in data:
        try:
            supplier = get_supplier(item, suppliers)

            # the factory turns the saved type back into the correct subclass
            # weight or download size is whichever one was saved for this product
            
            extra_value = item.get("weight", item.get("download_size", 0.0))
            product = ProductFactory.create(item.get("type"), item["id"], item["name"],
                                            item["price"], item["stock"], supplier, extra_value)

        except ValueError as error:     # unknown product type
            print(f"Skipping a product: {error}")
            continue
        except (KeyError, TypeError, AttributeError):
            print("Skipping a product with missing details.")
            continue
        inventory.add_product(product)

    print("Inventory loaded successfully.")
    return inventory


def save_inventory(inventory: Inventory) -> bool:
    """Write every product to inventory.json. Return True if it worked."""
    data = [product.to_dict() for product in inventory.get_products()]

    try:
        os.makedirs(DATA_DIR, exist_ok=True)
        with open(DATA_FILE, "w") as file:
            json.dump(data, file, indent=4)
        return True
    
    except OSError as error:
        print(f"Could not save inventory: {error}")
        return False