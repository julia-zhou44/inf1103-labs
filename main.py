# main.py
import math

from file_handling import load_inventory, save_inventory
from inventory import LINE
from product import Product

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


def add_product_menu(inventory):
    print("\nAdd New Product")

    product_id = get_product_id("Product ID: ")
    if product_id == "":
        print("Product ID cannot be empty.")
        return
    if inventory.search_product(product_id) is not None:  # check early so the user doesn't type everything for nothing
        print(f"Product ID {product_id} already exists.")
        return

    name = " ".join(input("Product Name: ").split())
    if name == "":
        print("Product name cannot be empty.")
        return

    price = get_valid_price()
    if price is None:
        return

    stock = get_valid_stock("Stock Quantity: ")
    if stock is None:
        return

    product = Product(product_id, name, price, stock)  # create the object
    inventory.add_product(product)                     # hand it to the inventory
    print("\nProduct added successfully!")


def update_stock_menu(inventory):
    print("\nUpdate Stock")
    product = inventory.search_product(get_product_id("Enter Product ID: "))

    if product is None:
        print("\nProduct not found.")
        return

    print("\nProduct Found:")
    print(f"Name: {product.get_name()}")
    print(f"Current Stock: {product.get_stock()}\n")

    new_stock = get_valid_stock("New Stock Quantity: ")
    if new_stock is None:
        return

    if product.update_stock(new_stock):  # the Product changes its own stock
        print("\nStock updated successfully!")


def search_product_menu(inventory):
    print("\nSearch Product")
    product = inventory.search_product(get_product_id("Enter Product ID: "))

    if product is None:
        print("\nProduct not found.")
        return

    print("\nProduct Found")
    print(LINE)
    product.display_information()
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
            inventory.display_all()
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
