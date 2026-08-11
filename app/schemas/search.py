from pydantic import BaseModel, Field
from typing import Optional


class SearchRequest(BaseModel):
    query: str = Field(..., min_length=1, description="عبارت جستجو")
    budget: Optional[float] = Field(None, description="حداکثر بودجه")
    limit: int = Field(10, ge=1, le=50, description="تعداد نتایج")
    providers: Optional[list[str]] = Field(
        None, description="فیلتر بر اساس نام provider"
    )


class SearchResultItem(BaseModel):
    title: str
    price: Optional[float] = None
    currency: str
    url: Optional[str] = None
    source: str
    region: str
    image_url: Optional[str] = None
    extra: dict = {}


class SearchResponse(BaseModel):
    query: str
    total: int
    results: list[SearchResultItem]
