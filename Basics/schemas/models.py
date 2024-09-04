from typing import Optional
from pydantic import BaseModel, Field

class Product:
    id: int
    name: str
    category: str
    description: str
    price: float

    def __init__(self, id, name, category, description, price):
        self.id = id
        self.name = name
        self.category = category
        self.description = description
        self.price = price

class ProductRequest(BaseModel):
    id: Optional[int] = None
    name: str = Field(min_length=1)
    category: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    price: float = Field(gt=0)  # Price must be greater than 0

    class Config:
        json_schema_extra = {
            'example': {
                'name': 'Innovative Widget',
                'category': 'Widgets',
                'description': 'An innovative widget that solves all your widget needs',
                'price': 19.99
            }
        }
