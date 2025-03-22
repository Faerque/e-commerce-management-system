import uuid


class Address:

    def __init__(self, street: str, city: str, state: str, postal_code: str, country: str):
        self.id = str(uuid.uuid4())
        self.street = street
        self.city = city
        self.state = state
        self.postal_code = postal_code
        self.country = country

    def __str__(self) -> str:
        return f"{self.street}, {self.city}, {self.state}, {self.postal_code}, {self.country}"
