from typing import Any, Dict, List, Optional

from app.adapters.stores.base_store import BaseStoreAdapter


class DigikalaAdapter(BaseStoreAdapter):
    @property
    def store_key(self) -> str:
        return "digikala"

    @property
    def store_name_fa(self) -> str:
        return "دیجی‌کالا"

    def search(
        self,
        query: str,
        filters: Optional[Dict[str, Any]] = None,
        limit: int = 20,
    ) -> List[Dict[str, Any]]:
        """
        Temporary mock output for integration wiring.
        In next step, we'll connect this to digikala_legacy.py logic.
        """
        filters = filters or {}
        min_price = filters.get("min_price")
        max_price = filters.get("max_price")

        items: List[Dict[str, Any]] = [
            {
                "title": f"{query} - مدل A",
                "price": 25_000_000,
                "url": "https://www.digikala.com/product/dkp-mock-a/",
                "store": self.store_key,
                "availability": "in_stock",
                "score": 4.3,
                "specs": {"brand": "ASUS", "ram": "8GB"},
            },
            {
                "title": f"{query} - مدل B",
                "price": 42_000_000,
                "url": "https://www.digikala.com/product/dkp-mock-b/",
                "store": self.store_key,
                "availability": "in_stock",
                "score": 4.5,
                "specs": {"brand": "Lenovo", "ram": "16GB"},
            },
        ]

        # very simple filter pass (temporary)
        if min_price is not None:
            items = [x for x in items if x.get("price") is not None and x["price"] >= min_price]
        if max_price is not None:
            items = [x for x in items if x.get("price") is not None and x["price"] <= max_price]

        return items[:limit]
