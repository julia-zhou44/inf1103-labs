import json
import os

from inventory import Inventory
from product import Product

DATA_DIR = "data"
DATA_FILE = os.path.join(DATA_DIR, "inventory.json")


def load_inventory():
    """Read inventory.json and return a filled Inventory object."""
    inventory = Inventory()

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
            # turn each dictionary from the file into a Product object
            product = Product(item["id"], item["name"], item["price"], item["stock"])
        except (KeyError, TypeError):
            print("Skipping a product with missing details.")
            continue
        inventory.add_product(product)

    print("Inventory loaded successfully.")
    return inventory


def save_inventory(inventory):
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