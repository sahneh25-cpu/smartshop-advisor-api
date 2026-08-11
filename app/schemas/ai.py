from pydantic import BaseModel, Field


class ProductQuestionsRequest(BaseModel):
    product_name: str = Field(..., min_length=2, max_length=100)


class ProductQuestion(BaseModel):
    key: str
    label: str
    type: str
    options: list[str] = []
    help_text: str | None = None


class ProductQuestionsResponse(BaseModel):
    product_type: str
    questions: list[ProductQuestion]
