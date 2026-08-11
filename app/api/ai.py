import os

from fastapi import APIRouter, Depends

from app.schemas.ai import ProductQuestionsRequest, ProductQuestionsResponse
from app.services.ai_provider_factory import get_ai_provider
from app.services.product_question_service import ProductQuestionService

router = APIRouter(prefix="/api/v1/ai", tags=["AI"])


def get_product_question_service() -> ProductQuestionService:
    provider_name = os.getenv("AI_PROVIDER", "local")
    provider = get_ai_provider(provider_name)
    return ProductQuestionService(provider)


@router.post("/product-questions", response_model=ProductQuestionsResponse)
def generate_product_questions(
    request: ProductQuestionsRequest,
    service: ProductQuestionService = Depends(get_product_question_service),
) -> ProductQuestionsResponse:
    return service.get_product_questions(request.product_name)


