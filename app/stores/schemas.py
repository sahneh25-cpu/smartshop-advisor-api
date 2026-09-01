from typing import Literal, Optional
from pydantic import BaseModel, HttpUrl

SearchType = Literal["marketplace", "aggregator", "classified", "retail"]


class StoreBase(BaseModel):
    name: str
    slug: str
    website: HttpUrl
    search_type: SearchType = "retail"
    is_active: bool = True
    priority: int = 100


class StoreCreate(StoreBase):
    pass


class StoreUpdate(BaseModel):
    name: Optional[str] = None
    slug: Optional[str] = None
    website: Optional[HttpUrl] = None
    search_type: Optional[SearchType] = None
    is_active: Optional[bool] = None
    priority: Optional[int] = None


class StoreOut(StoreBase):
    id: int
