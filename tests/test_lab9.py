# tests/test_lab9.py
# Lab 9 Section 7: automated tests for Strategy, Factory, validation and error handling.
# Run from the project folder:  python -m unittest discover -s tests -v

import io
import os
import tempfile
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

from digital_product import DigitalProduct
from discount import (BulkDiscount, DiscountStrategy, NoDiscount,
                      PercentageDiscount, StudentDiscount)
from file_handling import load_products
from inventory import Inventory
from main import get_non_negative_int, get_positive_float
from order import Order, OrderLine
from physical_product import PhysicalProduct
from product_factory import ProductFactory
from supplier import Supplier


def make_supplier() -> Supplier:
    return Supplier("S001", "Test Supplier", "test@example.com")


class TestDiscountStrategy(unittest.TestCase):
    """Order calculates totals through a DiscountStrategy (no if/elif in Order)."""

    def setUp(self) -> None:
        # an order whose lines add up to 250 (50 x 5)
        self.chair = ProductFactory.create("physical", "P1", "Chair", 50.0, 10,
                                           make_supplier(), 2.0)

    def make_order(self, discount: DiscountStrategy | None = None) -> Order:
        order = Order("1", discount)
        order.add_order_line(self.chair, 5)
        return order

    def test_no_discount_by_default(self) -> None:
        self.assertAlmostEqual(self.make_order().calculate_total(), 250.0)

    def test_percentage_discount(self) -> None:
        self.assertAlmostEqual(self.make_order(PercentageDiscount(10)).calculate_total(), 225.0)

    def test_bulk_discount_at_or_above_threshold(self) -> None:
        self.assertAlmostEqual(self.make_order(BulkDiscount(200, 20)).calculate_total(), 230.0)

    def test_bulk_discount_below_threshold(self) -> None:
        self.assertAlmostEqual(BulkDiscount(200, 20).apply(150), 150)

    def test_set_discount_replaces_strategy(self) -> None:
        order = self.make_order(BulkDiscount(200, 20))
        self.assertAlmostEqual(order.calculate_total(), 230.0)
        order.set_discount(PercentageDiscount(10))
        self.assertAlmostEqual(order.calculate_total(), 225.0)   # starts from 250 again, not 230

    def test_student_discount_without_changing_order(self) -> None:
        self.assertAlmostEqual(self.make_order(StudentDiscount()).calculate_total(), 237.5)

    def test_new_strategy_defined_here_works_with_order(self) -> None:
        # a brand-new strategy written only in this test: Order still works unchanged (OCP)
        class HalfPrice(DiscountStrategy):
            def apply(self, total: float) -> float:
                return total / 2
        self.assertAlmostEqual(self.make_order(HalfPrice()).calculate_total(), 125.0)

    def test_two_orders_can_share_one_strategy(self) -> None:
        shared = PercentageDiscount(10)
        self.assertAlmostEqual(self.make_order(shared).calculate_total(), 225.0)
        self.assertAlmostEqual(self.make_order(shared).calculate_total(), 225.0)


class TestProductFactory(unittest.TestCase):
    """Products are created through ProductFactory; unknown types raise ValueError."""

    def test_creates_physical_product(self) -> None:
        product = ProductFactory.create("physical", "P1", "Lamp", 25.0, 10, make_supplier(), 1.5)
        self.assertIsInstance(product, PhysicalProduct)
        self.assertEqual(product.get_weight(), 1.5)

    def test_creates_digital_product(self) -> None:
        product = ProductFactory.create("digital", "D1", "E-Book", 9.9, 100, make_supplier(), 15.0)
        self.assertIsInstance(product, DigitalProduct)
        self.assertEqual(product.get_download_size(), 15.0)

    def test_unknown_type_raises_clear_value_error(self) -> None:
        with self.assertRaises(ValueError) as context:
            ProductFactory.create("service", "S1", "Installation", 30.0, 5, make_supplier())
        self.assertIn("Unknown product type: service", str(context.exception))


class TestValidation(unittest.TestCase):
    """Invalid prices, stock quantities and order quantities are rejected."""

    def setUp(self) -> None:
        self.supplier = make_supplier()

    def test_zero_price_rejected(self) -> None:
        with self.assertRaises(ValueError):
            ProductFactory.create("physical", "P1", "Lamp", 0, 10, self.supplier)

    def test_negative_price_rejected(self) -> None:
        with self.assertRaises(ValueError):
            ProductFactory.create("physical", "P1", "Lamp", -5.0, 10, self.supplier)

    def test_negative_stock_rejected(self) -> None:
        with self.assertRaises(ValueError):
            ProductFactory.create("digital", "D1", "E-Book", 9.9, -1, self.supplier)

    def test_zero_stock_allowed(self) -> None:
        product = ProductFactory.create("digital", "D1", "E-Book", 9.9, 0, self.supplier)
        self.assertEqual(product.get_stock(), 0)

    def test_update_stock_rejects_negative_and_keeps_old_value(self) -> None:
        for product_type in ("physical", "digital"):        # LSP: same rule for both subclasses
            product = ProductFactory.create(product_type, "X1", "Item", 10.0, 5, self.supplier)
            with self.assertRaises(ValueError):
                product.update_stock(-3)
            self.assertEqual(product.get_stock(), 5)

    def test_order_line_quantity_must_be_positive(self) -> None:
        product = ProductFactory.create("physical", "P1", "Lamp", 10.0, 5, self.supplier)
        for bad_quantity in (0, -2):
            with self.assertRaises(ValueError):
                OrderLine(product, bad_quantity)
            with self.assertRaises(ValueError):
                Order("1").add_order_line(product, bad_quantity)


class TestUserInput(unittest.TestCase):
    """Invalid user input is handled without crashing, and the user is asked again."""

    @patch("builtins.input", side_effect=["abc", "-5", "12.50"])
    def test_get_positive_float_retries_until_valid(self, mock_input) -> None:
        output = io.StringIO()
        with redirect_stdout(output):
            value = get_positive_float("Price: ")
        self.assertEqual(value, 12.5)
        self.assertEqual(mock_input.call_count, 3)            # asked three times
        self.assertIn("Please enter a valid number", output.getvalue())
        self.assertIn("Please enter a number greater than zero", output.getvalue())

    @patch("builtins.input", side_effect=["ten", "-1", "7"])
    def test_get_non_negative_int_retries_until_valid(self, mock_input) -> None:
        with redirect_stdout(io.StringIO()):
            value = get_non_negative_int("Stock: ")
        self.assertEqual(value, 7)
        self.assertEqual(mock_input.call_count, 3)


class TestLoadProducts(unittest.TestCase):
    """Missing files are handled; bad rows are reported and skipped; valid rows still load."""

    CSV_CONTENT = (
        "product_type,product_id,name,price,stock_quantity\n"
        "physical,P001,Desk Lamp,25.00,10\n"
        "digital,D001,Photo Editor,49.90,100\n"
        "service,S001,Installation,30.00,5\n"
        "physical,P002,Office Chair,abc,3\n"
        "physical,P003,Monitor Stand,39.50,7\n"
    )

    def setUp(self) -> None:
        # write the lab's CSV to a temporary folder, so the tests don't depend on products.csv
        self.temp_dir = tempfile.TemporaryDirectory()
        self.csv_path = os.path.join(self.temp_dir.name, "products.csv")
        with open(self.csv_path, "w", newline="") as file:
            file.write(self.CSV_CONTENT)

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_valid_rows_load_and_bad_rows_are_skipped(self) -> None:
        inventory = Inventory()
        output = io.StringIO()
        with redirect_stdout(output):
            load_products(self.csv_path, inventory, make_supplier())

        loaded_ids = [p.get_product_id() for p in inventory.get_products()]
        self.assertEqual(loaded_ids, ["P001", "D001", "P003"])
        text = output.getvalue()
        self.assertIn("Unknown product type: service", text)
        self.assertIn("could not convert string to float: 'abc'", text)
        self.assertIn("3 products loaded.", text)
        self.assertTrue(text.strip().endswith("Load attempt finished."))   # finally runs last

    def test_missing_file_is_handled_gracefully(self) -> None:
        inventory = Inventory()
        output = io.StringIO()
        missing_path = os.path.join(self.temp_dir.name, "does_not_exist.csv")
        with redirect_stdout(output):
            load_products(missing_path, inventory, make_supplier())   # must not raise

        text = output.getvalue()
        self.assertIn("Products file not found", text)
        self.assertIn("Load attempt finished.", text)       # finally still runs
        self.assertNotIn("products loaded", text)           # else did not run
        self.assertEqual(inventory.get_products(), [])


if __name__ == "__main__":
    unittest.main()
