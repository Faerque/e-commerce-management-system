from typing import List

from src.product_handler import Product
from src.users_handler import User


class CartItem:

    def __init__(self, product: Product, quantity: int):
        self.product = product
        self._quantity = quantity

    @property
    def quantity(self) -> int:
        return self._quantity

    @quantity.setter
    def quantity(self, value: int):
        if value < 0:
            raise ValueError("Quantity cant be negative")
        if value > self.product.stock_quantity:
            raise ValueError("Quantity cant be exceed available stock")
        self._quantity = value

    @property
    def sub_total(self) -> float:
        return self.product.price * self._quantity


class Cart:

    def __init__(self, user: User):
        self.user = user,
        self.items: List[CartItem] = []  # Wallet, Pen

    def add_item(self, product: Product, quantity: int = 1) -> bool:

        if product.stock_quantity < quantity:
            return False

        existing_item = next(
            (item for item in self.items if item.product == product), None)

        if existing_item:
            existing_item.quantity += quantity
        else:
            self.items.append(CartItem(product, quantity))

    def remove_item(self, product: Product):
        self.items = [item for item in self.items if item.product != product]

    def clear(self):
        self.items.clear()

    def update_quantity(self, product: Product, quantity: int) -> bool:
        item = next(
            (item for item in self.items if item.product == product), None)

        if item:
            item.quantity = quantity
            return True
        return False

    @property
    def total(self) -> float:
        return sum(item.sub_total for item in self.items)
