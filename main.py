from typing import Dict, List, Optional

from src.address_handler import Address
from src.categories_handler import Category
from src.enums import OrderStatus, PaymentMethod, PaymentStatus, UserRole
from src.orders_handler import Order
from src.payment_handler import CreditCardProcessor, PaymentProcessor
from src.product_handler import Product
from src.users_handler import User


class EcommerceSystem:

    def __init__(self):
        self.users: List[User] = []
        self.products: List[Product] = []
        self.categories: List[Category] = []
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

    def process_payment(self, order: Order, payment_method: PaymentMethod, payment_info: Dict) -> bool:
        process = self.payment_processor.get(payment_method)

        if not process:
            return False

        if process.process_payment(order.total, payment_info):
            order.status = OrderStatus.CONFIRMED
            order.payment_method = payment_method

            return True
        order.payment_method = PaymentStatus.FAILED
        return False

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
    system.categories.extend([electronics, phones])

    # Register users
    admin = system.register_user(
        'John', 'John@example.com', "123456", UserRole.ADMIN)
    vendor = system.register_user(
        'Doe', 'Doe@example.com', "123456", UserRole.VENDOR)
    customer = system.register_user(
        'Mark', 'mark@example.com', "123456", UserRole.CUSTOMER)

    print(f'Users: {admin.username}, {vendor.username}, {customer.username}')

    for category in system.categories:
        print(f'{category.name}')

    # Add product
    print("=============Adding Product============")
    i_phone_1 = Product('Iphone 1', "Latest Iphone model",
                        899.99, phones, vendor)
    i_phone_1.add_stock(10)
    system.products.append(i_phone_1)

    # Add address for customer
    print("=============Adding address for customer============")
    customer.add_address(
        Address("123 street", "CTG", "state", "4212", "Bangladesh"))

    # Adding product to customer cart
    print("=============Customer adding product============")
    customer.cart.add_item(i_phone_1)

    order = system.create_order(customer, customer.addresses[0])

    if order:

        payment_info = {
            "card_number": "1234567890123456",
            "expriy": "12/28",
            "CVV": "101",
        }

        if system.process_payment(order, PaymentMethod.CREDIT_CARD, payment_info):
            print(f"Order {order.id} process successfully")
            print(f"Total amount ${order.total}")
        else:
            print("Payment process failed")

    else:
        print("Order creation failed")


if __name__ == "__main__":
    main()
