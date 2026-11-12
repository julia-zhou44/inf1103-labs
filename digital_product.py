# digital_product.py
from product import Product
from supplier import Supplier

class DigitalProduct(Product):


    def __init__(self, product_id: str, name: str, price: float, stock: int,
             download_size: float, supplier: Supplier):
        super().__init__(product_id, name, price, stock, supplier)  # reuse parent constructor

        self.__download_size: float = download_size # in MB

    def get_download_size(self) -> float:
        return self.__download_size

    def display_information(self) -> None:
        super().display_information()    # parent prints the common line
        print(f"    Type: Digital | Download Size: {self.__download_size} MB")


    def get_fulfilment_info(self) -> str:
        return "Delivered digitally via download link."

    def to_dict(self) -> dict:
        """Add the type and download size to the parent's dictionary (used when saving to JSON)."""
        data = super().to_dict()
        data["type"] = "digital"
        data["download_size"] = self.__download_size

        return data




    