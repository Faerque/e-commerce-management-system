from abc import ABC, abstractmethod
from typing import Dict

import re


class PaymentProcessor(ABC):

    @abstractmethod
    def process_payment(self, amount: float, payment_info: Dict) -> bool:
        pass

    @abstractmethod
    def refund_payment(self, amount: float, payment_info: Dict) -> bool:
        pass


class CreditCardProcessor(PaymentProcessor):

    def process_payment(self, amount: float, payment_info: Dict) -> bool:

        card_number = payment_info.get('card_number')
        if not card_number or not self._validate_card_number(card_number):
            return False
        return True

    def refund_payment(self, amount: float, payment_info: Dict) -> bool:
        return True

    def _validate_card_number(self, card_number: str) -> bool:

        return bool(re.match(r'^\d{16}$', card_number))
