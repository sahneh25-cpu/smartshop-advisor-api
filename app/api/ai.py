import os
from fastapi import APIRouter, Depends

from app.schemas.ai import (
    AdvisorRequest,
    AdvisorResponse,
    BrandListRequest,
    BrandListResponse,
    DynamicQuestionFlowRequest,
    DynamicQuestionsRequest,
    ProductQuestionsRequest,
    ProductQuestionsResponse,
)
from app.services.category_questions import brands_for, product_type_label
from app.services.advisor import AdvisorService
from app.services.ai_provider_factory import get_ai_provider
from app.services.product_question_service import ProductQuestionService

router = APIRouter(prefix="/api/v1/ai", tags=["AI"])


def get_product_question_service() -> ProductQuestionService:
    provider = get_ai_provider()
    return ProductQuestionService(provider=provider)


def get_advisor_service() -> AdvisorService:
    provider_name = os.getenv("AI_PROVIDER", "local")
    provider = get_ai_provider(provider_name)
    return AdvisorService(provider)


@router.post("/dynamic-questions", response_model=ProductQuestionsResponse)
def get_dynamic_questions(
    request: DynamicQuestionsRequest,
    service: ProductQuestionService = Depends(get_product_question_service),
):
    return service.get_dynamic_questions(
        user_query=request.user_query,
        current_answers=request.current_answers,
    )


@router.post("/dynamic-question-flow", response_model=ProductQuestionsResponse)
def dynamic_question_flow(
    request: DynamicQuestionFlowRequest,
    service: ProductQuestionService = Depends(get_product_question_service),
):
    return service.get_dynamic_questions(
        user_query=request.user_query,
        current_answers=request.answers,
    )


@router.post("/product-questions", response_model=ProductQuestionsResponse)
def product_questions(
    request: ProductQuestionsRequest,
    service: ProductQuestionService = Depends(get_product_question_service),
):
    name = (request.product_name or request.user_query or "").strip()
    return service.get_product_questions(name)


@router.post("/brands", response_model=BrandListResponse)
def list_brands(request: BrandListRequest) -> BrandListResponse:
    label = product_type_label(request.user_query)
    return BrandListResponse(product_type=label, brands=brands_for(request.user_query))


@router.post("/advisor/recommend", response_model=AdvisorResponse)
async def advisor_recommend(
    request: AdvisorRequest,
    service: AdvisorService = Depends(get_advisor_service),
) -> AdvisorResponse:
    return await service.recommend(request)
