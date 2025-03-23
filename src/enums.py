from enum import Enum


class UserRole(Enum):

    CUSTOMER = 'customer'
    ADMIN = 'admin'
    VENDOR = 'vendor'


class OrderStatus(Enum):
    """
    Defning States of customers order process
    """

    PENDING = 'pending'
    CONFIRMED = 'confirmed'
    SHIPPED = 'shipped'
    DELIVERD = 'delivred'
    CANCELLED = 'cancelled'


class PaymentMethod(Enum):
    """
    Defining payment method for payment
    """
    CREDIT_CARD = 'credit_card'
    DEBIT_CARD = 'debit_card'
    NET_BANKING = 'net_banking'
    WALLET = 'wallet'


class PaymentStatus(Enum):

    """
    Defning Payment Status of the order that place in system
    """

    PENDING = 'pending'
    COMPLETED = 'completed'
    FAILED = 'failed'
    REFUNDED = 'refunded'
