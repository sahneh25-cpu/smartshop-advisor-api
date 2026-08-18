from typing import List, Dict, Any

class ProductService:
    def __init__(self):
        # این لیست فعلاً نقش دیتابیس کوچک ما را بازی می‌کند
        self.products = [
            {"id": 1, "name": "iPhone 15 Pro", "price": 999.0, "category": "smartphone"},
            {"id": 2, "name": "Samsung Galaxy S24", "price": 899.0, "category": "smartphone"},
            {"id": 3, "name": "Google Pixel 8", "price": 699.0, "category": "smartphone"},
            {"id": 4, "name": "MacBook Air M2", "price": 1199.0, "category": "laptop"},
            {"id": 5, "name": "Dell XPS 13", "price": 1099.0, "category": "laptop"},
        ]

    def search_products(self, query: str) -> List[Dict[str, Any]]:
        # یک جستجوی بسیار ساده بر اساس نام محصول
        query = query.lower()
        results = [
            p for p in self.products 
            if query in p["name"].lower() or query in p["category"].lower()
        ]
        return results
