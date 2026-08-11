from fastapi import APIRouter, Query
from typing import Optional
from app.providers.registry import all_providers
from app.schemas.search import SearchResponse, SearchResultItem

router = APIRouter()

@router.get("/", response_model=SearchResponse, tags=["Search"])
async def search_products(
    q: str = Query(..., description="عبارت جستجو"),
    max_price: Optional[float] = Query(None, description="حداکثر قیمت"),
    limit: int = Query(20, ge=1, le=100, description="تعداد نتایج"),
):
    providers = all_providers()

    all_results = []
    for provider in providers:
        items = await provider.search(
            query=q,
            budget=max_price,
            limit=limit,
        )
        all_results.extend(items)

    return SearchResponse(
        query=q,
        total=len(all_results),
        results=[
            SearchResultItem(
                title=r.title,
                price=r.price,
                currency=r.currency,
                url=r.url,
                source=r.source,
                region=r.region,
                image_url=r.image_url,
                extra=r.extra,
            )
            for r in all_results
        ],
    )

