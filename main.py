# main.py
import math

from file_handling import load_inventory, save_inventory
from inventory import Inventory, LINE
from product_factory import ProductFactory
from supplier import Supplier

# menu choice -> (type name for the factory, prompt for that type's extra value)
PRODUCT_TYPE_OPTIONS: dict[str, tuple[str, str]] = {
    "1": ("physical", "Weight (kg): "),
    "2": ("digital", "Download Size (MB): "),
}

def get_product_id(prompt: str) -> str:
    """Ask for a product ID. 'p001' and 'P001' are treated the same."""
    return input(prompt).strip().upper()


def get_positive_float(prompt: str) -> float:
    """Keep asking until the user enters a number greater than zero (Section 5.1)
    float() raises ValueError for text like 'abc', so that is caught and the user is asked again"""

    while True:
        try:
            value = float(input(prompt))
            if not math.isfinite(value) or value <= 0:   # also blocks 'inf' and 'nan'
                print("Please enter a number greater than zero.")
                continue
            return round(value, 2)
        except ValueError:
            print("Please enter a valid number, e.g. 12.50")


def get_non_negative_int(prompt: str) -> int:
    """Keep asking until the user enters a whole number 0 or more (used for stock)"""
    while True:
        try:
            value = int(input(prompt))
            if value < 0:
                print("Please enter a whole number 0 or more.")
                continue
            return value
        except ValueError:
            print("Please enter a whole number, e.g. 10")


def get_supplier_for_product(inventory: Inventory) -> Supplier | None:
    """Ask for a supplier ID. Reuse the existing Supplier object if one already supplies a product """
    supplier_id = input("Supplier ID: ").strip().upper()
    if supplier_id == "":
        print("Supplier ID cannot be empty.")
        return None

    # if an existing product already has this supplier, reuse that same Supplier object
    for product in inventory.get_products():
        if product.get_supplier().get_supplier_id() == supplier_id:
            print(f"Using existing supplier: {product.get_supplier().get_name()}")
            return product.get_supplier()

    # otherwise create a new Supplier
    name = " ".join(input("Supplier Name: ").split())
    if name == "":
        print("Supplier name cannot be empty.")
        return None
    email = input("Supplier Email: ").strip()
    return Supplier(supplier_id, name, email)


def add_product_menu(inventory: Inventory) -> None:
    print("\nAdd New Product")

    product_id = get_product_id("Product ID: ")
    if product_id == "":
        print("Product ID cannot be empty.")
        return
    if inventory.find_product(product_id) is not None:  # check early so the user doesn't type everything for nothing
        print(f"Product ID {product_id} already exists.")
        return

    name = " ".join(input("Product Name: ").split())
    if name == "":
        print("Product name cannot be empty.")
        return

    price = get_positive_float("Price: ")              
    stock = get_non_negative_int("Stock Quantity: ")   # keeps asking until valid

    supplier = get_supplier_for_product(inventory)   
    if supplier is None:                             
        return  

    print("\nProduct Type:")
    print("1. Physical Product")
    print("2. Digital Product")
    choice = input("Enter type: ").strip()

    option = PRODUCT_TYPE_OPTIONS.get(choice)
    if option is None:
        print("Invalid product type. Please enter 1 or 2.")
        return
    product_type, extra_prompt = option

    extra_value = get_positive_float(extra_prompt)

    try:
        product = ProductFactory.create(product_type, product_id, name, price,
                                        stock, supplier, extra_value)
    except ValueError as error:
        print(f"Could not create product: {error}")
        return

    inventory.add_product(product)  # hand the object to the inventory
    print("\nProduct added successfully!")


def update_stock_menu(inventory: Inventory) -> None:
    print("\nUpdate Stock")
    product = inventory.find_product(get_product_id("Enter Product ID: "))

    if product is None:
        print("\nProduct not found.")
        return

    print("\nProduct Found:")
    print(f"Name: {product.get_name()}")
    print(f"Current Stock: {product.get_stock()}\n")

    new_stock = get_non_negative_int("New Stock Quantity: ")

    try:
        product.update_stock(new_stock)  # the Product checks and changes its own stock
    except ValueError as error:
        print(f"\nCould not update stock: {error}")
        return
    print("\nStock updated successfully!")


def search_product_menu(inventory: Inventory) -> None:
    print("\nSearch Product")
    product = inventory.find_product(get_product_id("Enter Product ID: "))

    if product is None:
        print("\nProduct not found.")
        return

    print("\nProduct Found")
    print(LINE)
    product.display_information()
    print()
    product.get_supplier().display_information()
    
    print(f"Fulfilment: {product.get_fulfilment_info()}")  # each product type describes itself
    print(LINE)

# ---------------- Menu system ----------------

def show_menu() -> None:
    print("\n---------- MENU ----------")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Save Inventory")
    print("6. Exit")
    print("--------------------------")


def main() -> None:
    print("=" * 37)
    print("INVENTORY MANAGEMENT SYSTEM")
    print("=" * 37 + "\n")

    inventory = load_inventory()  # Inventory object holding Physical and Digital products

    while True:
        show_menu()
        option = input("\nEnter option: ").strip()

        if option == "1":
            inventory.display_all_products()

        elif option == "2":
            add_product_menu(inventory)

        elif option == "3":
            update_stock_menu(inventory)

        elif option == "4":
            search_product_menu(inventory)

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