from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Dict, Any


class AdvisorInput(BaseModel):
    user_query: str
    user_answers: Dict[str, Any] = Field(default_factory=dict)
    search_results: List[Dict[str, Any]] = Field(default_factory=list)


class Question(BaseModel):
    id: str
    text: str


class UserIntent(BaseModel):
    product_type: Optional[str] = None
    budget: Optional[float] = None
    priorities: List[str] = Field(default_factory=list)
    extracted_features: Dict[str, Any] = Field(default_factory=dict)


class ProductQuestion(BaseModel):
    key: str
    label: str
    type: str
    options: List[str] = Field(default_factory=list)


class ProductQuestionsResponse(BaseModel):
    product_type: Optional[str] = None
    questions: List[ProductQuestion] = Field(default_factory=list)


class DynamicQuestionFlowRequest(BaseModel):
    user_query: str
    answers: Dict[str, Any] = Field(default_factory=dict)


class DynamicQuestionFlowResponse(BaseModel):
    product_type: Optional[str] = None
    next_questions: List[Question] = Field(default_factory=list)
    is_complete: bool = False
    summary: Optional[str] = None


class AIAdvisorResponse(BaseModel):
    message: str
    suggested_products: List[Dict[str, Any]] = Field(default_factory=list)
    follow_up_questions: List[str] = Field(default_factory=list)


class ProductQuestionsRequest(BaseModel):
    product_name: Optional[str] = None
    user_query: Optional[str] = None


class AdvisorRequest(BaseModel):
    user_query: str
    user_answers: Dict[str, Any] = Field(default_factory=dict)
    search_results: List[Dict[str, Any]] = Field(default_factory=list)


class Product(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    price: float


class AdvisorResponse(BaseModel):
    recommended_product: Optional[Product] = None
    reasoning: str
    alternatives: List[Product] = Field(default_factory=list)
