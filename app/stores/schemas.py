from typing import Literal, Optional
from pydantic import BaseModel, HttpUrl

SourceType = Literal["retail", "marketplace", "aggregator", "classified"]
ItemCondition = Literal["new", "used"]
SellerType = Literal["individual", "business"]
DomainScope = Literal["electronics", "appliances", "automotive", "general"]


class StoreBase(BaseModel):
    name: str
    slug: str
    website: HttpUrl
    source_type: SourceType = "retail"
    item_conditions: list[ItemCondition] = ["new"]
    seller_types: list[SellerType] = ["business"]
    domain_scope: DomainScope = "general"
    is_active: bool = True
    priority: int = 100


class StoreCreate(StoreBase):
    pass


class StoreUpdate(BaseModel):
    name: Optional[str] = None
    slug: Optional[str] = None
    website: Optional[HttpUrl] = None
    source_type: Optional[SourceType] = None
    item_conditions: Optional[list[ItemCondition]] = None
    seller_types: Optional[list[SellerType]] = None
    domain_scope: Optional[DomainScope] = None
    is_active: Optional[bool] = None
    priority: Optional[int] = None


class StoreOut(StoreBase):
    id: int
