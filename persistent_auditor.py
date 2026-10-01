import os

TAX_RATE = 0.10        # 10% tax per delivery
STORAGE_LIMIT = 500    # overstock limit
DATA_FILE = os.path.join("data", "inventory.txt")
FIRST_ORDER_ID = 1001  # order IDs start here

# Functions

def show_current_orders(total, history):
    """Print every saved order and the current total."""
    print("Current Orders:\n")
    if not history:
        print("(no orders yet)")
    for order_id, name, quantity in history:
        print(f"{order_id}, {name}, {quantity}")
    print(f"\nTotal Inventory: {total}")


def load_inventory():
    """Read saved total and order history. Return (0, []) if no file exists."""
    try:
        with open(DATA_FILE, "r") as file:
            lines = file.read().splitlines()
    except FileNotFoundError:
        print("No saved inventory found. Starting with an empty inventory.")
        return 0, []

    try:
        total = int(lines[0].split(":", 1)[1].strip())
        history = []
        for line in lines[1:]:
            if not line.strip():
                continue  # skip blank lines
            order_id, name, quantity = line.split(",")
            history.append([int(order_id), name.strip(), int(quantity)])
    except (IndexError, ValueError):
        print("Inventory file is unreadable. Starting with an empty inventory.")
        return 0, []

    show_current_orders(total, history)
    return total, history


def save_inventory(total, history):
    """Write final total and every order to the inventory file."""
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)  # create data/ if missing
    with open(DATA_FILE, "w") as file:
        file.write(f"Total Inventory: {total}\n")
        for order_id, name, quantity in history:
            file.write(f"{order_id},{name},{quantity}\n")
    print(f"\nOrder successfully saved to {DATA_FILE}")


def get_product_name():
    name = input("\nEnter Product Name (or 'quit' to exit): ").strip()

    if name.lower() == "quit":
        return "quit"

    name = " ".join(name.split())  # clear extra space: "wireless   mouse" -> "wireless mouse"

    if name == "" or not name.replace(" ", "").isalpha():  # letters and spaces only
        print("Invalid product name. Please use letters only.\n")
        return None

    return name.title()  # "mouse", "MOUSE", "mOuSe" all become "Mouse"


def get_valid_quantity():
    user_input = input("Enter Quantity: ").strip()

    if not user_input.removeprefix('-').isdigit():  # reject anything outside of numbers
        print("Invalid input, please enter numbers only.\n")
        return None

    elif int(user_input) < 0:  # reject negative numbers
        print("Error. Positive numbers only.\n")
        return None

    return int(user_input)


def next_order_id(history):
    """Continue numbering from the last saved order."""
    if history:
        return history[-1][0] + 1
    return FIRST_ORDER_ID


def process_delivery(current_total, new_value):
    return current_total + new_value


def calculate_tax(amount):
    return amount * TAX_RATE


def generate_report(total_units, failed_attempts, deliveries_processed, total_tax, history):
    print("\n--- Final Report ---")
    print(f"Total Deliveries Processed: {deliveries_processed}")
    print(f"Total Units Processed: {total_units}")
    print(f"Total Tax: {total_tax:.2f}")
    print(f"Number of Failed/Rejected Entries: {failed_attempts}")
    print(f"Transaction History (quantities): {[order[2] for order in history]}\n")


# ---------------- Main program ----------------

# load saved orders from file, and start this session's counters at zero
inventory, transaction_history = load_inventory()
total_units_processed = 0
deliveries_processed = 0
failed_entries = 0
total_tax = 0.0

while True:

    product_name = get_product_name()

    if product_name == "quit":  # user wants to exit
        break

    elif product_name is None:  # name rejected
        failed_entries += 1
        continue

    quantity = get_valid_quantity()

    if quantity is None:  # quantity rejected
        failed_entries += 1
        continue

    # valid order: record it, update total, calculate tax, update counters
    order_id = next_order_id(transaction_history)
    inventory = process_delivery(inventory, quantity)
    transaction_history.append([order_id, product_name, quantity])
    tax = calculate_tax(quantity)

    total_units_processed += quantity
    deliveries_processed += 1
    total_tax += tax

    print("\nNew Order Added:")
    print(f"{order_id},{product_name},{quantity}")

    if inventory > STORAGE_LIMIT:  # overstock alert
        print(f"STOP! You have exceeded storage space. Current Inventory {inventory}\n")
        break

    else:
        print(f"Tax for this order: {tax:.2f}. Current Inventory {inventory}")

save_inventory(inventory, transaction_history)
generate_report(total_units_processed, failed_entries, deliveries_processed,
                total_tax, transaction_history)