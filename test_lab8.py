# test_lab8.py 
# association, aggregation, composition, LSP, polymorphism

from supplier import Supplier
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from inventory import Inventory
from order import Order
from product import Product

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


def test_composition() -> None:
    print("\n=== 4. COMPOSITION: Order <>-- OrderLine ===")
    supplier = Supplier("S001", "Lenovo Pte Ltd", "sales@lenovo.com")
    keyboard = PhysicalProduct("P300", "Keyboard", 45.00, 25, 0.8, supplier)
    antivirus = DigitalProduct("D300", "Antivirus Licence", 59.90, 100, 850, supplier)

    order1 = Order("1")
    order1.add_order_line(keyboard, 2)
    order1.add_order_line(antivirus, 1)
    order1.display_order()

    # Predict first: same Product in two Orders -> how many OrderLines / Products?
    order2 = Order("2")
    order2.add_order_line(keyboard, 5)
    order2.display_order()

    line1 = order1.get_order_lines()[0]
    line2 = order2.get_order_lines()[0]
    print("\nSame Product object in both lines?", line1.get_product() is line2.get_product())
    print("Same OrderLine object?", line1 is line2)
    print("id(keyboard):", id(keyboard), "| id(line1):", id(line1), "| id(line2):", id(line2))

    order1.remove_order_line("P300")
    print("\nAfter removing the keyboard line from O001:")
    order1.display_order()
    print("Keyboard Product still exists:", keyboard.get_name())

def show_product_details(product: Product) -> None:
    """Works with ANY Product subclass — no isinstance checks."""
    product.display_information()
    print(product.get_fulfilment_info())


def test_lsp_and_polymorphism() -> None:
    print("\n=== 6 & 7. LSP + POLYMORPHISM ===")
    print()
    supplier = Supplier("S003", "GainCity", "GainCity@gmail.com")
    monitor = PhysicalProduct("P400", "Monitor", 299.99, 10, 5.0, supplier)
    editor = DigitalProduct("D400", "Photo Editor", 120.00, 30, 2048, supplier)

    print("show_product_details() called with each subclass:")
    show_product_details(monitor)
    show_product_details(editor)

    # both work through the Inventory too, using the Product abstraction
    inventory = Inventory()
    inventory.add_product(monitor)
    inventory.add_product(editor)

    print("\nupdate_stock() keeps the same meaning for both subclasses:")
    for product in inventory.get_products():
        accepted = product.update_stock(7)
        print(product.get_name(), "-> accepted:", accepted, "| stock now:", product.get_stock())

if __name__ == "__main__":
    test_association()
    test_aggregation()
    test_composition()
    test_lsp_and_polymorphism()