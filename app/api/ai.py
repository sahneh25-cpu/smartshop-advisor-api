import os
from fastapi import APIRouter, Depends
from app.schemas.ai import (
    DynamicQuestionFlowRequest,
    ProductQuestionsRequest,
    ProductQuestionsResponse,
    AdvisorRequest,
    AdvisorResponse,
    Product,
)
from app.services.ai_provider_factory import get_ai_provider
from app.services.product_question_service import ProductQuestionService
from app.services.advisor import AdvisorService
from app.services.product_service import ProductService
from app.schemas.ai import AdvisorInput

router = APIRouter(prefix="/api/v1/ai", tags=["AI"])


def get_product_question_service() -> ProductQuestionService:
    provider_name = os.getenv("AI_PROVIDER", "local")
    provider = get_ai_provider(provider_name)
    return ProductQuestionService(provider)


def get_advisor_service() -> AdvisorService:
    provider_name = os.getenv("AI_PROVIDER", "local")
    provider = get_ai_provider(provider_name)
    return AdvisorService(provider)


def get_product_service() -> ProductService:
    return ProductService()


@router.post("/product-questions", response_model=ProductQuestionsResponse)
def generate_product_questions(
    request: ProductQuestionsRequest,
    service: ProductQuestionService = Depends(get_product_question_service),
) -> ProductQuestionsResponse:
    return service.get_product_questions(request.product_name)


@router.post("/dynamic-question-flow", response_model=ProductQuestionsResponse)
def generate_dynamic_question_flow(
    request: DynamicQuestionFlowRequest,
    service: ProductQuestionService = Depends(get_product_question_service),
) -> ProductQuestionsResponse:
    return service.get_dynamic_questions(request.user_query)


@router.post("/advisor/recommend", response_model=AdvisorResponse)
async def advisor_recommend(
    request: AdvisorRequest,
    service: AdvisorService = Depends(get_advisor_service),
    product_service: ProductService = Depends(get_product_service),
) -> AdvisorResponse:
    search_results = request.search_results
    if not search_results and request.user_query:
        search_results = product_service.search_products(request.user_query)

    result = await service.recommend(
        AdvisorInput(
            user_query=request.user_query,
            user_answers=request.user_answers,
            search_results=search_results,
        )
    )

    recommended_product_obj = None
    reasoning_str = ""
    alternatives_list = []

    if isinstance(result, dict):
        raw_recommended_product = result.get("recommended_product")
        if raw_recommended_product:
            recommended_product_obj = Product(**raw_recommended_product)

        reasoning_str = result.get("reasoning") or ""

        raw_alternatives = result.get("alternatives", [])
        alternatives_list = [Product(**item) for item in raw_alternatives if item]
    else:
        recommended_product_obj = result.recommended_product
        reasoning_str = result.reasoning or ""
        alternatives_list = result.alternatives or []

    if recommended_product_obj is None and search_results:
        recommended_product_obj = Product(**search_results[0])

    if not alternatives_list and search_results:
        start_index = 1 if recommended_product_obj is not None else 0
        alternatives_list = [
            Product(**item) for item in search_results[start_index:] if item
        ]

    if not reasoning_str.strip():
        if recommended_product_obj is not None:
            reasoning_str = "Recommended based on the user's query and available search results."
        else:
            reasoning_str = "No suitable product was found based on the provided input."

    return AdvisorResponse(
        recommended_product=recommended_product_obj,
        reasoning=reasoning_str,
        alternatives=alternatives_list,
    )
