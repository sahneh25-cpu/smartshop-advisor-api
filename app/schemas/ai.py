from __future__ import annotations

from typing import Any, Dict, List, Literal, Optional
from pydantic import BaseModel, ConfigDict, Field, model_validator


class UserIntent(BaseModel):
    product_type: Optional[str] = None
    budget: Optional[float] = None
    priorities: List[str] = Field(default_factory=list)
    extracted_features: Dict[str, Any] = Field(default_factory=dict)
    missing_slots: List[str] = Field(default_factory=list)


class ProductQuestionOption(BaseModel):
    value: str = ""
    label: str = ""
    id: Optional[str] = None
    text: Optional[str] = None

    @model_validator(mode="before")
    @classmethod
    def coerce(cls, data: Any) -> Any:
        if isinstance(data, str):
            return {"value": data, "label": data, "id": data, "text": data}
        if isinstance(data, dict):
            value = data.get("value") or data.get("id") or data.get("text") or data.get("label") or ""
            label = data.get("label") or data.get("text") or value
            return {
                "value": str(value),
                "label": str(label),
                "id": str(data.get("id") or value),
                "text": str(data.get("text") or label),
            }
        return data


class ProductQuestion(BaseModel):
    id: str = ""
    key: str = ""
    text: str = ""
    label: str = ""
    type: str = "choice"
    options: List[ProductQuestionOption] = Field(default_factory=list)
    help_text: Optional[str] = None

    @model_validator(mode="after")
    def sync_aliases(self) -> "ProductQuestion":
        ident = self.id or self.key
        title = self.text or self.label
        self.id = ident
        self.key = ident
        self.text = title
        self.label = title
        return self


class DynamicQuestionsRequest(BaseModel):
    user_query: str
    current_answers: Dict[str, Any] = Field(default_factory=dict)


class DynamicQuestionFlowRequest(BaseModel):
    user_query: str
    answers: Dict[str, Any] = Field(default_factory=dict)


class ProductQuestionsRequest(BaseModel):
    user_query: Optional[str] = None
    product_name: Optional[str] = None


class ProductQuestionsResponse(BaseModel):
    product_type: Optional[str] = None
    questions: List[ProductQuestion] = Field(default_factory=list)


class DynamicQuestionFlowResponse(BaseModel):
    product_type: Optional[str] = None
    next_questions: List[ProductQuestion] = Field(default_factory=list)
    is_complete: bool = False


class BrandListRequest(BaseModel):
    user_query: str
    country: Optional[str] = None


class BrandListResponse(BaseModel):
    product_type: str
    brands: List[str]


class Product(BaseModel):
    """
    Unified offer model for retail + marketplace + classified sources.
    """
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    price: float

    currency: str = "IRR"
    brand: Optional[str] = None
    model_name: Optional[str] = None

    # condition-aware fields
    condition: Literal["new", "used", "refurbished"] = "new"
    source_type: Literal["retail", "aggregator", "classified", "marketplace"] = "retail"

    # trust/seller fields
    seller_name: Optional[str] = None
    seller_type: Optional[Literal["store", "individual", "unknown"]] = "unknown"
    seller_reputation: Optional[float] = Field(default=None, ge=0, le=5)

    # location/negotiation fields
    location: Optional[str] = None
    price_negotiable: bool = False

    # inventory/logistics
    availability: Optional[Literal["in_stock", "out_of_stock", "unknown"]] = "unknown"
    warranty_months: Optional[int] = Field(default=None, ge=0)

    # source linkage
    source_name: Optional[str] = None
    source_url: Optional[str] = None


class AdvisorInput(BaseModel):
    user_query: str
    user_answers: Dict[str, Any] = Field(default_factory=dict)
    search_results: List[Dict[str, Any]] = Field(default_factory=list)


class AdvisorRequest(AdvisorInput):
    pass


class AdvisorResponse(BaseModel):
    recommended_product: Optional[Product] = None
    reasoning: str
    alternatives: List[Product] = Field(default_factory=list)


# Pydantic v2: resolve forward refs / full model definitions
UserIntent.model_rebuild()
ProductQuestionOption.model_rebuild()
ProductQuestion.model_rebuild()
DynamicQuestionsRequest.model_rebuild()
DynamicQuestionFlowRequest.model_rebuild()
ProductQuestionsRequest.model_rebuild()
ProductQuestionsResponse.model_rebuild()
DynamicQuestionFlowResponse.model_rebuild()
BrandListRequest.model_rebuild()
BrandListResponse.model_rebuild()
Product.model_rebuild()
AdvisorInput.model_rebuild()
AdvisorRequest.model_rebuild()
AdvisorResponse.model_rebuild()
