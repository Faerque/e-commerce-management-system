from typing import List, Dict, Optional
from src.users_handler import User
from src.product_handler import Product
from src.categories_handler import Category
from src.orders_handler import Order
from src.address_handler import Address
from src.enums import PaymentMethod, PaymentStatus, UserRole
from src.payment_handler import PaymentProcessor, CreditCardProcessor


class EcommerceSystem:

    def __init__(self):
        self.users: List[User] = []
        self.products: List[Product] = []
        self.catgory: List[Category] = []
        self.orders: List[Order] = []
        self.payment_processor: Dict[PaymentMethod, PaymentProcessor] = {
            PaymentMethod.CREDIT_CARD: CreditCardProcessor()
        }

    def register_user(self, username: str, email: str, password: str, role: UserRole) -> User:

        if any(user.email == email for user in self.users):
            raise ValueError("Email already registered")

        if any(user.username == username for user in self.users):
            raise ValueError("Username already taken")

        user = User(username, email, password, role)
        self.users.append(user)

        return user

    def create_order(self, user: User, shipping_address: Address) -> Optional[Order]:

        if not user.cart.items:
            return None

        for cart_item in user.cart.items:
            if cart_item.quantity > cart_item.product.stock_quantity:
                return None

        order = Order(user, shipping_address)
        order.items = user.cart.items.copy()

        for item in order.items:
            item.product.remove_stock(item.quantity)

        user.cart.clear()

        self.orders.append(order)
        user.orders.append(order)

        return order

    def search_product(self, query: str, category: Optional[Category] = None) -> List[Product]:

        results = []

        for product in self.products:
            if (query.lower() in product.name.lower() or query.lower() in product.descrption.lower()):
                if category is None or product.category == category:
                    results.append(product)

        return results


def main():

    system = EcommerceSystem()

    # Create Catgories
    electronics = Category("Electronics", "Electronices device and accesories")
    phones = Category("Phone", "Mobile phones and accessories")
    electronics.add_subcategory(phones)
    system.catgory.extend([electronics, phones])

    # Register users
    admin = system.register_user(
        'John', 'John@example.com', "123456", UserRole.ADMIN)
    vendor = system.register_user(
        'Doe', 'Doe@example.com', "123456", UserRole.VENDOR)
