import uuid
from typing import List, Optional


class Category:

    """
    Category class, stores category name, and descprtions
    __Optional__
        subcategories and parent categories
    """

    def __init__(self, name: str, descriptions: str):
        self.id = str(uuid.uuid4())
        self.name = name
        self.descriptions = descriptions
        self.subcategories: List['Category'] = []
        self.parent: Optional['Category'] = None

    def add_subcategory(self, category: 'Category'):
        category.parent = self
        self.subcategories.append(category)
