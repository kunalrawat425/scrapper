# app/utils/cache.py
from typing import Dict, Any, Optional
import json
import os
from app.config import JSON_DB_PATH

class Cache:
    def __init__(self):
        self.cache = self._load_cache()

    def _load_cache(self) -> Dict[str, Any]:
        if os.path.exists(JSON_DB_PATH):
            with open(JSON_DB_PATH, 'r') as file:
                return {product['product_title']: product for product in json.load(file)}
        return {}

    def get(self, product_title: str) -> Optional[Dict[str, Any]]:
        return self.cache.get(product_title)

    def set(self, product_title: str, data: Dict[str, Any]):
        self.cache[product_title] = data
        self._save_cache()

    def _save_cache(self):
        with open(JSON_DB_PATH, 'w') as file:
            json.dump(list(self.cache.values()), file, indent=4)
