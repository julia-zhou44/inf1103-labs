# product_factory.py
# Factory pattern: one place that knows which Product subclasses exist
# rest of  program asks the factory for a Product and never names a subclass

from product import Product
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from supplier import Supplier


class ProductFactory:

    # maps each type name to its class; adding a new product type = one new line here
    __PRODUCT_CLASSES: dict[str, type[Product]] = {
        "physical": PhysicalProduct,
        "digital": DigitalProduct,
    }

    @staticmethod
    def create(product_type: str, product_id: str, name: str, price: float,
               stock: int, supplier: Supplier, extra_value: float = 0.0) -> Product:
        """Build and return a Product of the requested type.
        extra_value is the weight (kg) for physical products or download size (MB) for digital ones.
        Raises ValueError if the type is unknown."""
        product_class = ProductFactory.__PRODUCT_CLASSES.get(product_type)
        if product_class is None:
            raise ValueError(f"Unknown product type: {product_type}")
        return product_class(product_id, name, price, stock, extra_value, supplier)
