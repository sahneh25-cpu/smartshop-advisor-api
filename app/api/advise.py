from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.advise import AdviseRequest, AdviseResponse
from app.core.database import SessionLocal
from app.providers.registry import all_providers
from app.services.ai import GeminiService
import asyncio
import dataclasses

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/advise/", response_model=AdviseResponse)
async def get_ai_recommendations(request: AdviseRequest):
    # جستجوی موازی روی همه providers
    providers = all_providers()
    tasks = [
        p.search(query=request.query, budget=request.max_price, limit=request.limit)
        for p in providers
    ]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    products = []
    for r in results:
        if isinstance(r, list):
            for item in r:
                if dataclasses.is_dataclass(item) and not isinstance(item, type):
                    products.append(dataclasses.asdict(item))
                elif hasattr(item, "model_dump"):
                    products.append(item.model_dump())
                elif hasattr(item, "__dict__"):
                    products.append(item.__dict__)

    # فیلتر قیمت حداقل
    if request.min_price is not None:
        products = [p for p in products if (p.get("price") or 0) >= request.min_price]

    # تحلیل Gemini
    try:
        ai = GeminiService()
        ranked, explanation = ai.analyze_and_rank_products(
            query=request.query,
            products=products,
            use_case=request.use_case,
            priorities=request.priorities,
            smart_answers=request.smart_answers,
        )
    except Exception as e:
        ranked = products
        explanation = f"تحلیل هوشمند غیرفعال: {e}"

    return AdviseResponse(
        products=ranked[: request.limit],
        analysis=explanation,
        ranking_explanation=explanation,
    )
