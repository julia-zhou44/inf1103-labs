import os

TAX_RATE = 0.10        # 10% tax per delivery
STORAGE_LIMIT = 500    # overstock limit
DATA_FILE = os.path.join("data", "inventory.txt")

#Functions

def load_inventory():
    """Read saved total and history. Return (0, []) if no file exists."""
    try:
        with open(DATA_FILE, "r") as file:
            lines = file.read().splitlines()
    except FileNotFoundError:
        print("No saved inventory found. Starting with an empty inventory.")
        return 0, []

    try:
        total = int(lines[0].split(":", 1)[1].strip())
        history_text = lines[1].split(":", 1)[1].strip()
        history = [int(x) for x in history_text.split(",")] if history_text else []
    except (IndexError, ValueError):
        print("Inventory file is unreadable. Starting with an empty inventory.")
        return 0, []

    print(f"Loaded inventory: {total} units, {len(history)} past transactions.")
    return total, history

 
def get_valid_input():
    user_input = input("\nEnter Stock Quantity (or 'quit' to exit): ").strip()
 
    if user_input.lower() == "quit":  # Quit
        return "quit"
 
    elif not user_input.removeprefix('-').isdigit():  # reject anything outside of numbers
        print("Invalid input, please enter numbers only.\n")
        return None  # tell loop this entry failed
 
    elif int(user_input) < 0:  # reject negative numbers
        print("Error. Positive numbers only.\n")
        return None  # tell loop this entry failed
 
    return int(user_input)  # only reached if the input is valid
 
 
def process_delivery(current_total, new_value): #delivery
    new_total = current_total + new_value
    return new_total

 
def calculate_tax(amount): # tax
    return amount * TAX_RATE
 
 
# summary report

def generate_report(total_units, failed_attempts, deliveries_processed, total_tax, history):
    print("\n--- Final Report ---")
    print(f"Total Deliveries Processed: {deliveries_processed}")
    print(f"Total Units Processed: {total_units}")
    print(f"Total Tax: {total_tax:.2f}")
    print(f"Number of Failed/Rejected Entries: {failed_attempts}")
    print(f"Transaction History: {history}\n")

def save_inventory(total, history):
    """Write final total and full transaction history to the inventory file."""
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)  # create data/ if missing
    with open(DATA_FILE, "w") as file:
        file.write(f"Total Inventory: {total}\n")
        file.write("Transaction History: " + ",".join(str(x) for x in history) + "\n")
    print(f"Inventory saved to {DATA_FILE}")
 
# ---------------- Main program ----------------
 
# initialise inventory and counters to zero at the start
inventory, transaction_history = load_inventory()
total_units_processed = 0
deliveries_processed = 0
failed_entries = 0
total_tax = 0.0
 
while True:
    
    response = get_valid_input()
 
    if response == "quit":  # user wants to exit
        break
 
    elif response is None:  #  input rejected by get_valid_input()
        failed_entries += 1
 
    else:
        if inventory + response > STORAGE_LIMIT:  # overstock: reject this delivery
            print(f"STOP! This delivery would exceed storage space. Current Inventory {inventory}\n")
            failed_entries += 1
            continue
        
        # valid delivery: update total, calculate tax, update counters
        inventory = process_delivery(inventory, response)
        transaction_history.append(response)
        tax = calculate_tax(response)
        
        
 
        total_units_processed += response
        deliveries_processed += 1
        total_tax += tax
 
        if inventory > STORAGE_LIMIT:  # overstock alert
            print(f"STOP! You have exceeded storage space. Current Inventory {inventory}\n")
            break
 
        else:
            print(f"Registered. Tax for this delivery: {tax:.2f}. Current Inventory {inventory}")

save_inventory(inventory, transaction_history)
generate_report(total_units_processed, failed_entries, deliveries_processed, total_tax, transaction_history)
