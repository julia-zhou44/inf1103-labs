# file_handling.py
import json
import os

from inventory import Inventory
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
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
            # use the saved "type" to rebuild the correct subclass
            product_type = item.get("type")
            
            if product_type == "physical":
                product = PhysicalProduct(item["id"], item["name"], item["price"],
                                          item["stock"], item["weight"])
                
            elif product_type == "digital":
                product = DigitalProduct(item["id"], item["name"], item["price"],
                                         item["stock"], item["download_size"])
                
            else:
                print(f"Skipping a product with unknown type: {product_type}")
                continue
        
        except (KeyError, TypeError, AttributeError):
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