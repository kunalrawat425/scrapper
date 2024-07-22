from typing import Dict, Optional
from app.schemas.product import Product

class Cache:
    def __init__(self):
        self._cache: Dict[str, Product] = {}

    def get(self, key: str) -> Optional[Product]:
        return self._cache.get(key)

    def set(self, key: str, value: Product):
        self._cache[key] = value

    def clear(self):
        self._cache.clear()
