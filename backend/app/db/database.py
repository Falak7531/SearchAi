"""
db/database.py - Simple JSON-based product database abstraction.
Provides CRUD-like access to product data stored in a JSON file.
Swap this out for PostgreSQL/MongoDB in production.
"""

import json
import os
from typing import List, Optional, Dict
from app.models.product import Product

PRODUCTS_FILE = os.environ.get(
    "PRODUCTS_PATH",
    os.path.join(os.path.dirname(__file__), "../../../data/products.json"),
)


class ProductDatabase:
    """In-memory product store loaded from a JSON file."""

    def __init__(self, file_path: str = PRODUCTS_FILE):
        self.file_path = file_path
        self._products: Dict[str, dict] = {}
        self._load()

    def _load(self):
        """Load products from JSON file into memory."""
        try:
            with open(self.file_path, "r") as f:
                products = json.load(f)
                self._products = {p["id"]: p for p in products}
            print(f"✅ Loaded {len(self._products)} products from database.")
        except FileNotFoundError:
            print(f"⚠️  Products file not found at {self.file_path}. Starting with empty DB.")
            self._products = {}

    def get_all(self) -> List[dict]:
        return list(self._products.values())

    def get_by_id(self, product_id: str) -> Optional[dict]:
        return self._products.get(product_id)

    def get_by_ids(self, ids: List[str]) -> List[dict]:
        return [self._products[pid] for pid in ids if pid in self._products]

    def filter_by_category(self, category: str) -> List[dict]:
        return [p for p in self._products.values() if p.get("category") == category]

    def count(self) -> int:
        return len(self._products)


# Singleton instance
db = ProductDatabase()
