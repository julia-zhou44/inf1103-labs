# test_lab8.py - 
# association, aggregation, composition, LSP, polymorphism
from supplier import Supplier
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from inventory import Inventory


def test_association() -> None:
    print("\n=== 2. ASSOCIATION: Supplier <-> Product ===")
    supplier = Supplier("S001", "Lenovo Pte Ltd", "Lenovo@gmail.com")
    laptop = PhysicalProduct("P100", "Laptop", 1200.00, 10, 2.5, supplier)
    ebook = DigitalProduct("D100", "Python E-Book", 29.90, 50, 15.0, supplier)

    # display the supplier information through each Product
    laptop.get_supplier().display_information()
    ebook.get_supplier().display_information()

    # confirm they are separate objects
    print("Both products share the same Supplier object?",
          laptop.get_supplier() is ebook.get_supplier())
    print("Supplier and Product are separate objects?", supplier is not laptop)

    # Predict first: what happens after del supplier?
    del supplier
    print("After 'del supplier':")
    laptop.get_supplier().display_information()


def test_aggregation() -> None:
    print("\n=== 3. AGGREGATION: Inventory <>-- Product ===")
    supplier = Supplier("S002", "HP", "HP@gmail.com")

    # 1. create the Product b4 any Inventory exists
    mouse = PhysicalProduct("P200", "Mouse", 25.50, 40, 0.1, supplier)

    inventory_a = Inventory()
    inventory_b = Inventory()

    # 2. add it to Inventory A
    inventory_a.add_product(mouse)
    print("In Inventory A:", inventory_a.find_product("P200") is not None)

    # 3. remove it from A and check the Product still works (need predict first)
    inventory_a.remove_product("P200")
    print("In Inventory A after removal:", inventory_a.find_product("P200") is not None)
    print("Product still usable after removal:")
    mouse.display_information()

    # 4. add the SAME object to Inventory B
    inventory_b.add_product(mouse)
    print("Same object now in Inventory B:", inventory_b.find_product("P200") is mouse)


if __name__ == "__main__":
    test_association()
    test_aggregation()