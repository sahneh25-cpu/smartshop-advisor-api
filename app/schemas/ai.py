from typing import Any, Dict, List, Optional, Union

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


class BrandListRequest(BaseModel):
    user_query: str
    country: Optional[str] = None


class BrandListResponse(BaseModel):
    product_type: str
    brands: List[str]


class Product(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    price: float


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
