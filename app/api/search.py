from fastapi import APIRouter, Query
from typing import Optional, Literal
from app.services.store_search_service import StoreSearchService
from app.schemas.search import SearchResponse, SearchResultItem

router = APIRouter()

@router.get("/", response_model=SearchResponse, tags=["Search"])
async def search_products(
    q: str = Query(..., description="عبارت جستجو"),
    min_price: Optional[float] = Query(None, description="حداقل قیمت"),
    max_price: Optional[float] = Query(None, description="حداکثر قیمت"),
    limit: int = Query(20, ge=1, le=100, description="تعداد نتایج"),
    sort_by: str = Query("best_value", description="ستون مرتبسازی (price, spec_score, best_value)"),
    sort_order: Literal["asc", "desc"] = Query("desc", description="ترتیب مرتبسازی"),
):
    service = StoreSearchService()

    # ساخت دیکشنری فیلترها به صورت داینامیک
    search_filters = {}
    if min_price is not None:
        search_filters["min_price"] = min_price
    if max_price is not None:
        search_filters["max_price"] = max_price

    all_results = service.search_all(
        query=q,
        filters=search_filters,
        limit_per_store=limit,
        sort_by=sort_by,
        sort_order=sort_order,
    )

    return SearchResponse(
        query=q,
        total=len(all_results),
        results=[
            SearchResultItem(
                title=r.get("title"),
                price=r.get("price"),
                currency=r.get("currency", "IRR"),
                url=r.get("url"),
                source=r.get("store", r.get("source", "unknown")),
                region=r.get("region", "IR"),
                image_url=r.get("image_url"),
                extra=r.get("extra", {}),
            )
            for r in all_results
        ],
    )
