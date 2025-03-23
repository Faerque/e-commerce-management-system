from src.enums import UserRole
from typing import List, Optional, TYPE_CHECKING
import uuid
import hashlib
from src.shopping_cart_handler import Cart


if TYPE_CHECKING:
    from src.address_handler import Address
    from src.product_handler import Product
    from src.orders_handler import Order


class User:

    def __init__(self, username: str, email: str, password: str, role: UserRole = UserRole.CUSTOMER):
        self.id = str(uuid.uuid4())
        self.username = username,
        self.email = email,
        self._password_hash = self._hash_password(password),
        self.role = role,
        self.addresses: List['Address'] = []
        self.cart: Cart = Cart(self)
        self.wishlist: List['Product'] = []
        self.orders: List[Order] = []

    def _hash_password(self, password: str) -> str:
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        return hashed_password

    def verify_password(self, password: str) -> bool:
        return self._password_hash == self._hash_password(password)

    def add_address(self, address: 'Address'):
        self.addresses.append(address)

    def add_to_wishlist(self, product: 'Product'):
        if product not in self.wishlist:
            self.wishlist.append(product)

    def remove_from_wishlist(self, product: 'Product'):
        if product in self.wishlist:
            self.wishlist.remove(product)
