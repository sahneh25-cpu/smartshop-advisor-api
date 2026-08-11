import httpx
from app.providers.base import BaseProvider, ProductResult

TOROB_SEARCH_URL = "https://api.torob.com/v4/base-product/search/"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "application/json",
}


class TorobProvider(BaseProvider):
    name = "torob"
    region = "IR"

    async def search(self, query: str, budget: float | None = None, limit: int = 10) -> list[ProductResult]:
        params = {"q": query, "page": 1}

        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(
                TOROB_SEARCH_URL, params=params, headers=HEADERS
            )
            response.raise_for_status()
            data = response.json()

        results = []
        for item in data.get("results", [])[:limit]:
            # FIX: price ممکنه int یا float باشه، مستقیم از ریشه
            price_raw = item.get("price")
            try:
                price = float(price_raw) if price_raw is not None else None
            except (ValueError, TypeError):
                price = None

            if budget is not None and price is not None and price > budget:
                continue

            # FIX: image_url مستقیم در ریشه item است، نه داخل media_urls
            image_url = item.get("image_url") or item.get("image")

            # FIX: fallback برای media_urls اگر ساختار قدیمی بود
            if not image_url:
                for media in item.get("media_urls", []):
                    if isinstance(media, dict) and media.get("type") == "image":
                        image_url = media.get("url")
                        break
                    elif isinstance(media, str):
                        image_url = media
                        break

            relative_url = item.get("web_client_absolute_url", "")
            full_url = (
                f"https://torob.com{relative_url}" if relative_url else None
            )

            results.append(
                ProductResult(
                    title=item.get("name1") or item.get("name2", ""),
                    price=price,
                    currency="IRR",
                    url=full_url,
                    source=self.name,
                    region=self.region,
                    image_url=image_url,
                    extra={
                        "name2": item.get("name2"),
                        "price_text": item.get("price_text"),
                        "shop_text": item.get("shop_text"),
                        "stock_status": item.get("stock_status"),
                        "is_authentic": item.get("is_authentic"),
                    },
                )
            )

        return results
