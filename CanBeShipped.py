# can_be_shipped.py
from abc import ABC, abstractmethod


class CanBeShipped(ABC):
    """Interface: any class that can be shipped must calculate a shipping cost."""

    @abstractmethod
    def calculate_shipping_cost(self) -> float:
        """Return a non negative shipping charge."""