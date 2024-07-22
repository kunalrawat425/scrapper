from pydantic import BaseModel
from typing import Optional

class Product(BaseModel):
    product_title: str
    product_price: float
    path_to_image: str
