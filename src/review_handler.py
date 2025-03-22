
from src.users_handler import User
from src.product_handler import Product
import uuid
from datetime import datetime


class Review:

    def __init__(self, user: User, product: Product, rating: int, comment: str):
        self.id = str(uuid.uuid4())
        self.user = user
        self.product = product
        self.rating = min(max(rating, 1), 5)
        self.comment = comment
        self.timestamp = datetime.now()
