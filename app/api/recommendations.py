from decimal import Decimal
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.product import Product

router = APIRouter()


class RecommendationRequest(BaseModel):
    query: str = Field(..., min_length=2, description="عبارت جستجوی کاربر")
    budget_min: Optional[Decimal] = Field(None, description="حداقل بودجه")
    budget_max: Optional[Decimal] = Field(None, description="حداکثر بودجه")
    preferred_brands: List[str] = Field(default_factory=list, description="برندهای ترجیحی")
    preferred_keywords: List[str] = Field(default_factory=list, description="ویگی های اولویت دار")
    limit: int = Field(default=5, ge=1, le=20, description="تعداد نتایج")


class RecommendationItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    product_id: int
    product_name: str
    unit_price: Decimal
    category_name: Optional[str] = None
    match_score: int = Field(..., ge=0, le=100)
    reasons: List[str] = Field(default_factory=list)


class RecommendationResponse(BaseModel):
    query_summary: str
    recommendations: List[RecommendationItem]
    ai_summary: str


def _safe_text(value: Optional[str]) -> str:
    return (value or "").strip().lower()


def _score_product(product: Product, req: RecommendationRequest) -> tuple[int, List[str]]:
    score = 0
    reasons: List[str] = []

    query_text = _safe_text(req.query)
    product_name = _safe_text(getattr(product, "name", ""))
    product_desc = _safe_text(getattr(product, "description", ""))
    brand_name = _safe_text(getattr(product, "brand", ""))

    query_tokens = [token for token in query_text.split() if token]
    if query_tokens:
        matched_tokens = [
            token for token in query_tokens
            if token in product_name or token in product_desc
        ]
        if matched_tokens:
            query_score = min(40, len(matched_tokens) * 10)
            score += query_score
            reasons.append(f"مرتبط با جستجوی کاربر: {', '.join(matched_tokens)}")

    matched_keywords = []
    for kw in req.preferred_keywords:
        kw_norm = _safe_text(kw)
        if kw_norm and (kw_norm in product_name or kw_norm in product_desc):
            matched_keywords.append(kw)
    if matched_keywords:
        kw_score = min(30, len(matched_keywords) * 8)
        score += kw_score
        reasons.append(f"ویگی های اولویت دار مطابق: {', '.join(matched_keywords)}")

    matched_brands = []
    for brand in req.preferred_brands:
        brand_norm = _safe_text(brand)
        if brand_norm and brand_norm in brand_name:
            matched_brands.append(brand)
    if matched_brands:
        score += 15
        reasons.append(f"برند ترجیحی مطابق: {', '.join(matched_brands)}")

    price = getattr(product, "price", None)
    if price is not None:
        if req.budget_min is not None and price < req.budget_min:
            score -= 5
            reasons.append("کمتر از بودجه حداقل کاربر است")
        if req.budget_max is not None and price > req.budget_max:
            score -= 10
            reasons.append("بالاتر از بودجه حداکثر کاربر است")
        if req.budget_min is not None and req.budget_max is not None:
            if req.budget_min <= price <= req.budget_max:
                score += 10
                reasons.append("در بازه بودجه کاربر قرار دارد")

    category_name = _safe_text(getattr(getattr(product, "category", None), "name", ""))
    if query_tokens and category_name:
        if any(token in category_name for token in query_tokens):
            score += 10
            reasons.append(f"با دسته بندی {category_name} هم خوانی دارد")

    if not reasons:
        reasons.append("تطابق عمومی با نیازهای جستجو")

    return max(0, min(100, score)), reasons


def _ai_summary(req: RecommendationRequest, results: List[RecommendationItem]) -> str:
    if not results:
        return "هیچ کالایی با معیارهای فعلی پیدا نشد."
    best = results[0]
    return (
        f"بهترین گزینه فعلا «{best.product_name}» است "
        f"با امتیاز تطابق {best.match_score}/100. "
        f"این نتیجه بر اساس جستجوی «{req.query}» و اولویت های ثبت شده کاربر ساخته شده است."
    )


@router.post(
    "/recommendations/",
    response_model=RecommendationResponse,
    tags=["Recommendations"],
    summary="پیشنهاد کالا بر اساس جستجوی کاربر",
)
def get_recommendations(
    req: RecommendationRequest,
    db: Session = Depends(get_db),
):
    products = db.query(Product).all()

    if not products:
        raise HTTPException(
            status_code=404,
            detail="هیچ محصولی در پایگاه داده موجود نیست",
        )

    results: List[RecommendationItem] = []

    for product in products:
        score, reasons = _score_product(product, req)
        if score <= 0:
            continue

        category_name = None
        category = getattr(product, "category", None)
        if category is not None:
            category_name = getattr(category, "name", None)

        results.append(
            RecommendationItem(
                product_id=getattr(product, "id"),
                product_name=getattr(product, "name", ""),
                unit_price=getattr(product, "price"),
                category_name=category_name,
                match_score=score,
                reasons=reasons,
            )
        )

    results.sort(key=lambda item: item.match_score, reverse=True)
    results = results[: req.limit]

    budget_parts = []
    if req.budget_min is not None:
        budget_parts.append(f"از {req.budget_min:,.0f}")
    if req.budget_max is not None:
        budget_parts.append(f"تا {req.budget_max:,.0f}")

    query_summary = f"جستجو: {req.query}"
    if budget_parts:
        query_summary += " | بودجه: " + " ".join(budget_parts)

    return RecommendationResponse(
        query_summary=query_summary,
        recommendations=results,
        ai_summary=_ai_summary(req, results),
    )
