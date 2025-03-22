from src.categories_handler import Category
from src.users_handler import User
from src.review_handler import Review
from typing import List, Optional
import uuid


class Product:
    def __init__(self, name: str, descriptions: str, price: float, category: Category, vendor: User):
        self.id = str(uuid.uuid4())
        self.name = name
        self.descrption = descriptions
        self._price = price
        self.vendor = vendor
        self.stock_quantity = 0
        self.reviews: List['Review'] = []
        self.image: List[str] = []
        self.is_active = True

    @property
    def price(self) -> float:
        return self._price

    @price.setter
    def price(self, value: float):
        if value < 0:
            raise ValueError("Price cant be negative")
        self._price = value

    def add_stock(self, quantity: int) -> bool:
        if quantity < 0:
            raise ValueError("Quantity cant be negative")
        self.stock_quantity += quantity

    def remove_stock(self, quantity: int) -> bool:
        if quantity <= self.stock_quantity:
            self.stock_quantity -= quantity
            return True
        return False

    def add_review(self) -> float:
        if not self.reviews:
            return 0.0
        return sum(review.rating for review in self.reviews) / len(self.reviews)
