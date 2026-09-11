inventory = 0
total_units_processed = 0 
failed_entries = 0


while True:

    user_input = input("\nEnter Stock Quantity ( or 'quit' to exit'): ")

    if user_input.lower() == "quit": # incase Quit
           break

    elif not user_input.lstrip('-').isdigit(): # reject anything outside of numbers
           print("Invalid input, please enter numbers only.\n")
           failed_entries += 1

    elif int(user_input) < 0: # reject negative numbers
          print("Error. Positive numbers only.\n")
          failed_entries += 1

    else:
          quantity = int(user_input)
          inventory += quantity
          total_units_processed += quantity

          if inventory > 500: # overstock alert 
            print(f"STOP! You have exceeded storage space. Current Inventory {inventory}\n")
            break

          else:
               print(f"Registered. Current Inventory {inventory}")

print("\n--- Final Report ---")
print(f"Total Units Processed: {total_units_processed}")
print(f"Number of Failed/Rejected Entries: {failed_entries}")

           




    


