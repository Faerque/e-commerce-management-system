
from src.address_handler import Address
from src.shopping_cart_handler import CartItem
from typing import List, Optional, TYPE_CHECKING
import uuid

from src.enums import OrderStatus, PaymentMethod

from datetime import datetime

if TYPE_CHECKING:
    from src.users_handler import User


class Order:

    def __init__(self, user: "User", shipping_address: Address):
        self.id = str(uuid.uuid4())
        self.user = user
        self.items: List[CartItem] = []
        self.shipping_address = shipping_address
        self.order_date = datetime.now()
        self.status = OrderStatus.PENDING
        self.payment_method: Optional[PaymentMethod] = None
        self.shipping_cost = 0.0
        self.tracking_number: Optional[str] = None

    @property
    def subtotal(self) -> float:
        return sum(item.subtotal for item in self.items)

    @property
    def total(self) -> float:
        return self.subtotal + self.shipping_cost

    def add_tracking_number(self, tracking_number: str):
        self.tracking_number = tracking_number
        self.status = OrderStatus.SHIPPED

    def cancel_order(self) -> bool:
        if self.status in [OrderStatus.PENDING, OrderStatus.CONFIRMED]:
            self.status = OrderStatus.CANCELLED
            for item in self.items:
                item.product.add_stock(item.quantity)
            return True
        return False
