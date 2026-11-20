# discount.py
# Strategy pattern: each discount type is its own class with the same apply() method
# so Order can use any of them without knowing how they work

from abc import ABC, abstractmethod


class DiscountStrategy(ABC):
    """Abstract strat: every discount must provide apply()"""

    @abstractmethod
    def apply(self, total: float) -> float:
        pass


class NoDiscount(DiscountStrategy):
    """default - total stays same"""
    def apply(self, total: float) -> float:
        return total


class PercentageDiscount(DiscountStrategy):
    """takes a % off, eg PercentageDiscount(10) = 10% off"""

    def __init__(self, percent: float) -> None:
        self.__percent: float = percent

    def apply(self, total: float) -> float:
        return total * (1 - self.__percent / 100)


class BulkDiscount(DiscountStrategy):
    """takes fixed amt off if the total reaches a threshold,
    eg BulkDiscount(200, 20) = $20 off totals of $200 or more."""

    def __init__(self, threshold: float, amount: float) -> None:
        self.__threshold: float = threshold   # minimum total needed
        self.__amount: float = amount         # how much to take off

    def apply(self, total: float) -> float:
        if total >= self.__threshold:
            return total - self.__amount
        return total


class StudentDiscount(PercentageDiscount):
    """Section 2.4: new strategy added without changing Order
    student discount is 5% percentage discount, so it reuses PercentageDiscount"""

    def __init__(self) -> None:
        super().__init__(5)


# quick check: only runs when this file is run directly
if __name__ == "__main__":
    print(BulkDiscount(200, 20).apply(250))    # expected 230
    print(BulkDiscount(200, 20).apply(150))    # expected 150 (below threshold)
    print(PercentageDiscount(10).apply(250))   # expected 225.0
    print(StudentDiscount().apply(100))        # expected 95.0