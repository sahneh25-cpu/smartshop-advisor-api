from pydantic import BaseModel, Field
from typing import Optional, List


class AdviseRequest(BaseModel):
    query: str = Field(..., description="عبارت جستجو")
    use_case: Optional[str] = Field(None)
    priorities: Optional[List[str]] = Field(default_factory=list)
    smart_answers: Optional[dict] = Field(default_factory=dict)
    min_price: Optional[float] = Field(None, ge=0)
    max_price: Optional[float] = Field(None, ge=0)
    limit: int = Field(10, ge=1, le=50)


class AdviseResponse(BaseModel):
    products: List[dict]
    analysis: Optional[str] = None
    ranking_explanation: Optional[str] = None
