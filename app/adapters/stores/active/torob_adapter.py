from typing import Any, Dict, List, Optional

from app.adapters.stores.base_store import BaseStoreAdapter


class TorobAdapter(BaseStoreAdapter):
    @property
    def store_key(self) -> str:
        return "torob"

    @property
    def store_name_fa(self) -> str:
        return "ترب"

    def search(
        self,
        query: str,
        filters: Optional[Dict[str, Any]] = None,
        limit: int = 20,
    ) -> List[Dict[str, Any]]:
        filters = filters or {}
        min_price = filters.get("min_price")
        max_price = filters.get("max_price")

        items: List[Dict[str, Any]] = [
            {
                "title": f"{query} - فروشنده ۱",
                "price": 24_500_000,
                "url": "https://torob.com/p/mock-a/",
                "store": self.store_key,
                "availability": "in_stock",
                "score": 4.1,
                "specs": {"brand": "Acer", "ram": "8GB"},
            },
            {
                "title": f"{query} - فروشنده ۲",
                "price": 39_900_000,
                "url": "https://torob.com/p/mock-b/",
                "store": self.store_key,
                "availability": "in_stock",
                "score": 4.4,
                "specs": {"brand": "Lenovo", "ram": "16GB"},
            },
        ]

        if min_price is not None:
            items = [x for x in items if x.get("price") is not None and x["price"] >= min_price]
        if max_price is not None:
            items = [x for x in items if x.get("price") is not None and x["price"] <= max_price]

        return items[:limit]
