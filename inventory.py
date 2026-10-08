import json
import math
import os

# The JSON file lives in data/ so Docker can mount that folder as a volume.
# If the container is destroyed, the file stays on your computer.
DATA_DIR = "data"
DATA_FILE = os.path.join(DATA_DIR, "inventory.json")
LINE = "-" * 45


# ---------------- Data persistence ----------------

def load_inventory():
    """Load the product list from inventory.json. Return [] if the file is missing or unreadable."""
    if not os.path.exists(DATA_FILE):
        print("inventory.json not found. Starting with an empty inventory.")
        return []

    print("inventory.json found.")
    try:
        with open(DATA_FILE, "r") as file:
            inventory = json.load(file)
    except (json.JSONDecodeError, OSError):
        print("inventory.json is unreadable. Starting with an empty inventory.")
        return []

    if not isinstance(inventory, list):  # file must hold a list of product dictionaries
        print("inventory.json has the wrong format. Starting with an empty inventory.")
        return []

    print("Inventory loaded successfully.")
    return inventory


def save_inventory(inventory):
    """Write the whole product list to inventory.json. Return True if the save worked."""
    try:
        os.makedirs(DATA_DIR, exist_ok=True)  # create data/ if it doesn't exist yet
        with open(DATA_FILE, "w") as file:
            json.dump(inventory, file, indent=4)  # indent=4 keeps the file readable
        return True
    except OSError as error:
        print(f"Could not save inventory: {error}")
        return False


# ---------------- Input helpers ----------------

def find_product(inventory, product_id):
    """Return the product dictionary with this ID, or None if it doesn't exist."""
    for product in inventory:
        if product["id"] == product_id:
            return product
    return None


def get_product_id(prompt):
    """Ask for a product ID. 'p001' and 'P001' are treated the same."""
    return input(prompt).strip().upper()


def get_valid_price():
    """Ask for a price. Return a float rounded to 2 decimals, or None if invalid."""
    user_input = input("Price: ").strip()
    try:
        price = float(user_input)
    except ValueError:
        print("Invalid price. Please enter a number.")
        return None

    if not math.isfinite(price) or price < 0:  # blocks negatives, 'inf' and 'nan'
        print("Invalid price. Please enter a positive number.")
        return None

    return round(price, 2)


def get_valid_stock(prompt):
    """Ask for a stock quantity. Return a whole number 0 or more, or None if invalid."""
    user_input = input(prompt).strip()

    if not user_input.isdigit():  # rejects letters, decimals and negative signs
        print("Invalid quantity. Please enter a whole number (0 or more).")
        return None

    return int(user_input)


# ---------------- Data manipulation ----------------

def display_all(inventory):
    """Print every product in the inventory."""
    print("\nCurrent Inventory")
    print(LINE)
    if not inventory:
        print("(no products in inventory)")
    for product in inventory:
        print(f"ID: {product['id']} | Name: {product['name']} | "
              f"Price: ${product['price']:.2f} | Stock: {product['stock']}")
    print(LINE)


def add_product(inventory):
    """Ask for a new product's details and add it to the inventory as a dictionary."""
    print("\nAdd New Product")

    product_id = get_product_id("Product ID: ")
    if product_id == "":
        print("Product ID cannot be empty.")
        return
    if find_product(inventory, product_id):  # IDs must be unique
        print(f"Product ID {product_id} already exists.")
        return

    name = " ".join(input("Product Name: ").split())  # clear extra spaces
    if name == "":
        print("Product name cannot be empty.")
        return

    price = get_valid_price()
    if price is None:
        return

    stock = get_valid_stock("Stock Quantity: ")
    if stock is None:
        return

    # each product is a dictionary, stored inside the inventory list
    inventory.append({"id": product_id, "name": name, "price": price, "stock": stock})
    print("\nProduct added successfully!")


def update_stock(inventory):
    """Find a product by ID and replace its stock quantity."""
    print("\nUpdate Stock")
    product_id = get_product_id("Enter Product ID: ")
    product = find_product(inventory, product_id)

    if product is None:
        print("\nProduct not found.")
        return

    print("\nProduct Found:")
    print(f"Name: {product['name']}")
    print(f"Current Stock: {product['stock']}\n")

    new_stock = get_valid_stock("New Stock Quantity: ")
    if new_stock is None:
        return

    product["stock"] = new_stock  # changes the dictionary inside the list directly
    print("\nStock updated successfully!")


def search_product(inventory):
    """Find a product by ID and show its full details."""
    print("\nSearch Product")
    product_id = get_product_id("Enter Product ID: ")
    product = find_product(inventory, product_id)

    if product is None:
        print("\nProduct not found.")
        return

    print("\nProduct Found")
    print(LINE)
    print(f"ID: {product['id']}")
    print(f"Name: {product['name']}")
    print(f"Price: ${product['price']:.2f}")
    print(f"Stock: {product['stock']}")
    print(LINE)


# ---------------- Menu system ----------------

def show_menu():
    print("\n---------- MENU ----------")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Save Inventory")
    print("6. Exit")
    print("--------------------------")


def main():
    print("=" * 37)
    print("INVENTORY MANAGEMENT SYSTEM")
    print("=" * 37 + "\n")

    inventory = load_inventory()  # list of product dictionaries

    while True:
        show_menu()
        option = input("\nEnter option: ").strip()

        if option == "1":
            display_all(inventory)
        elif option == "2":
            add_product(inventory)
        elif option == "3":
            update_stock(inventory)
        elif option == "4":
            search_product(inventory)
        elif option == "5":
            print("\nSaving inventory...")
            if save_inventory(inventory):
                print("Inventory saved successfully to inventory.json.")
        elif option == "6":
            # always save on exit so no changes are lost
            print("\nSaving inventory before exit...")
            if save_inventory(inventory):
                print("Inventory saved successfully.")
            print("\nThank you for using Inventory Management System.")
            print("Program terminated.")
            break
        else:
            print("Invalid option. Please enter a number from 1 to 6.")


# only run the menu when this file is run directly (not when imported)
if __name__ == "__main__":
    main()
