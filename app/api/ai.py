from typing import Any, Dict, List
from fastapi import APIRouter, Depends
from app.schemas.ai import AdvisorInput, AdvisorResponse

router = APIRouter(prefix="/ai", tags=["AI"])

def get_advisor_service():
    from app.services.ai import AdvisorService
    return AdvisorService()

def get_ai_service():
    from app.services.ai import GeminiService
    return GeminiService()

@router.post("/advisor/recommend", response_model=AdvisorResponse)
async def advisor_recommend(payload: AdvisorInput, advisor_service=Depends(get_advisor_service)):
    return await advisor_service.recommend(payload)

@router.post("/dynamic-question-flow")
async def dynamic_question_flow(payload: Dict[str, Any]):
    user_query = (payload.get("user_query") or "").strip()
    q = user_query.replace("\u200c", " ").lower()

    if ("لپ تاپ" in q) or ("لپتاپ" in q):
        product_type = "لپ تاپ"
    elif ("گوشی" in q) or ("موبایل" in q):
        product_type = "گوشی موبایل"
    else:
        product_type = "محصول"

    questions: List[Dict[str, Any]] = [
        {"key": "budget", "question": "بودجه شما حدوداً چقدر است"},
        {"key": "brand_preference", "question": "برند مورد علاقهتان چیست"},
        {"key": "usage", "question": "کاربری اصلی شما چیست"},
    ]

    budget_markers = ["بودجه", "میلیون", "تومان", "million", "budget", "قیمت"]
    if any(m in q for m in budget_markers):
        questions = [x for x in questions if x["key"] != "budget"]

    return {"product_type": product_type, "questions": questions}

@router.post("/product-questions")
async def product_questions(payload: Dict[str, Any]):
    product_type = payload.get("product_type") or payload.get("product_name") or "محصول"
    return {
        "product_type": product_type,
        "questions": [
            {"key": "budget", "question": "بودجه شما چقدر است"},
            {"key": "priority", "question": "مهمترین ویگی مدنظر شما چیست"},
            {"key": "brand_preference", "question": "ترجیح برند شما چیست"},
        ],
    }
