from decimal import Decimal
from typing import Optional, Any
from pydantic import BaseModel

class ProductCreate(BaseModel):
    name: str
    price: Decimal
    description: Optional[str] = None
    category_id: Optional[int] = None
    attributes: Optional[dict[str, Any]] = None

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[Decimal] = None
    description: Optional[str] = None
    category_id: Optional[int] = None
    attributes: Optional[dict[str, Any]] = None

class ProductOut(BaseModel):
    id: int
    name: str
    price: Decimal
    description: Optional[str] = None
    category_id: Optional[int] = None
    attributes: Optional[dict[str, Any]] = None

    model_config = {"from_attributes": True}
