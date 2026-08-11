import httpx
from typing import Optional
from app.providers.base import BaseProvider, ProductResult

DIGIKALA_SEARCH_URL = "https://api.digikala.com/v1/search/"

class DigikalaProvider(BaseProvider):
    name = "digikala"
    region = "IR"

    async def search(
        self,
        query: str,
        limit: int = 10,
        budget: Optional[float] = None,
    ) -> list[ProductResult]:
        try:
            async with httpx.AsyncClient(timeout=25.0) as client:
                resp = await client.get(
                    DIGIKALA_SEARCH_URL,
                    params={"q": query, "page": 1},
                    headers={"User-Agent": "Mozilla/5.0"},
                )
            if resp.status_code != 200:
                return []

            data = resp.json().get("data", {})
            raw_products = data.get("products", [])

        except (httpx.TimeoutException, httpx.HTTPError, ValueError):
            return []

        results: list[ProductResult] = []

        for item in raw_products:
            if item.get("status") != "marketable":
                continue

            # عنوان
            title = item.get("title_fa") or item.get("title_en") or ""

            # URL
            uri = (item.get("url") or {}).get("uri", "")
            url = f"https://www.digikala.com{uri}" if uri else None

            # قیمت
            price: Optional[float] = None
            try:
                price = float(
                    item["default_variant"]["price"]["selling_price"]
                )
            except (KeyError, TypeError, ValueError):
                pass

            # فیلتر بودجه
            if budget is not None and price is not None and price > budget:
                continue

            # تصویر
            image_url: Optional[str] = None
            try:
                img = item["images"]["main"]["url"]
                image_url = img[0] if isinstance(img, list) else img
            except (KeyError, TypeError):
                pass

            # اطلاعات اضافه
            extra: dict = {
                "id": item.get("id"),
                "title_en": item.get("title_en"),
                "status": item.get("status"),
                "discount_percent": None,
                "rating": None,
                "seller": None,
            }
            try:
                extra["discount_percent"] = item["default_variant"]["price"]["discount_percent"]
            except (KeyError, TypeError):
                pass
            try:
                extra["rating"] = item["default_variant"]["rate"]["value"]
            except (KeyError, TypeError):
                pass
            try:
                extra["seller"] = item["default_variant"]["seller"]["title"]
            except (KeyError, TypeError):
                pass

            results.append(
                ProductResult(
                    title=title,
                    url=url,
                    source="digikala",
                    region="IR",
                    price=price,
                    currency="IRR",
                    image_url=image_url,
                    extra=extra,
                )
            )

            if len(results) >= limit:
                break

        return results
