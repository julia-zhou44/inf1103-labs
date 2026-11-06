TAX_RATE = 0.10        # 10% tax per delivery
STORAGE_LIMIT = 500    # overstock limit
 
 #Functions

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
def generate_report(total_units, failed_attempts, deliveries_processed, total_tax):
    print("\n--- Final Report ---")
    print(f"Total Deliveries Processed: {deliveries_processed}")
    print(f"Total Units Processed: {total_units}")
    print(f"Total Tax: {total_tax:.2f}")
    print(f"Number of Failed/Rejected Entries: {failed_attempts}\n")
 
 
# ---------------- Main program ----------------
 
# initialise inventory and counters to zero at the start
inventory = 0
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
        # valid delivery: update total, calculate tax, update counters
        inventory = process_delivery(inventory, response)
        tax = calculate_tax(response)
 
        total_units_processed += response
        deliveries_processed += 1
        total_tax += tax
 
        if inventory > STORAGE_LIMIT:  # overstock alert
            print(f"STOP! You have exceeded storage space. Current Inventory {inventory}\n")
            break
 
        else:
            print(f"Registered. Tax for this delivery: {tax:.2f}. Current Inventory {inventory}")
 
generate_report(total_units_processed, failed_entries, deliveries_processed, total_tax)
 