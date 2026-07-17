from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from decimal import Decimal
from pydantic import BaseModel, Field
from app.core.database import get_db
from app.models.product import Product
from app.models.category import Category

router = APIRouter()

class RecommendationRequest(BaseModel):
    diameter_mm: int = Field(..., description="قطر لوله مورد نیاز (میلیمتر)", example=110)
    pipe_length_m: float = Field(..., description="طول مورد نیاز (متر)", example=50.0)
    budget: Optional[Decimal] = Field(None, description="بودجه کل (تومان)", example=5000000)
    material: Optional[str] = Field(None, description="جنس لوله: PVC, UPVC, PE, CI", example="PVC")
    application: Optional[str] = Field(None, description="کاربرد: gravity_sewer, pressure_main, house_connection", example="gravity_sewer")

class RecommendationItem(BaseModel):
    product_id: int
    product_name: str
    unit_price: Decimal
    estimated_total: Decimal
    category_name: Optional[str]
    match_score: int = Field(..., description="امتیاز تطابق 0-100")
    reasons: List[str] = Field(..., description="دلایل توصیه")

    class Config:
        from_attributes = True

class RecommendationResponse(BaseModel):
    query_summary: str
    recommendations: List[RecommendationItem]
    engineering_notes: List[str]

def calculate_match_score(product: Product, req: RecommendationRequest) -> tuple[int, list[str]]:
    score = 0
    reasons = []
    name_lower = product.name.lower()

    if str(req.diameter_mm) in product.name:
        score += 40
        reasons.append(f"قطر {req.diameter_mm}mm با مشخصات محصول مطابقت دارد")

    if req.material:
        if req.material.lower() in name_lower:
            score += 30
            reasons.append(f"جنس {req.material} در مشخصات محصول موجود است")

    if req.budget is not None:
        estimated_total = product.price * Decimal(str(req.pipe_length_m))
        if estimated_total <= req.budget:
            score += 20
            reasons.append(f"برآورد هزینه {estimated_total:,.0f} تومان در محدوده بودجه است")
        else:
            score -= 10
            reasons.append(f"برآورد هزینه {estimated_total:,.0f} تومان از بودجه فراتر میرود")

    if req.application:
        application_keywords = {
            "gravity_sewer": ["فاضلاب", "گرانیتی", "جاذب"],
            "pressure_main": ["تحت فشار", "آبرسانی", "pressure"],
            "house_connection": ["انشعاب", "خانگی", "house"],
        }
        keywords = application_keywords.get(req.application, [])
        for kw in keywords:
            if kw in name_lower or (product.description and kw in product.description.lower()):
                score += 10
                reasons.append(f"مناسب برای کاربرد {req.application}")
                break

    if not reasons:
        reasons.append("محصول عمومی — نیاز به بررسی دستی دارد")

    return max(0, min(100, score)), reasons

def get_engineering_notes(req: RecommendationRequest) -> List[str]:
    notes = []

    if req.diameter_mm < 100:
        notes.append("⚠️ قطر کمتر از 100mm برای شبکه اصلی فاضلاب توصیه نمیشود (استاندارد EN 1401)")
    elif req.diameter_mm >= 200:
        notes.append("✅ قطر مناسب برای خط اصلی جمعآوری فاضلاب")

    if req.application == "gravity_sewer":
        notes.append("📐 شیب حداقل 1:100 برای خودپاکی لوله رعایت شود")
        notes.append("🔧 عمق حداقل 1.2 متر برای حفاظت در برابر یخبندان")

    if req.application == "pressure_main":
        notes.append("🔒 آزمون فشار هیدرواستاتیک 1.5 برابر فشار کاری الزامی است")

    if req.pipe_length_m > 100:
        notes.append(f"📦 برای طول {req.pipe_length_m}m اتصالات و واشر را در برآورد لحاظ کنید (~10% اضافه)")

    return notes

@router.post(
    "/recommendations/",
    response_model=RecommendationResponse,
    tags=["Recommendations"],
    summary="توصیه محصول بر اساس پارامترهای فنی"
)
def get_recommendations(req: RecommendationRequest, db: Session = Depends(get_db)):
    products = db.query(Product).all()

    if not products:
        raise HTTPException(status_code=404, detail="هیچ محصولی در پایگاه داده موجود نیست")

    results: List[RecommendationItem] = []

    for product in products:
        score, reasons = calculate_match_score(product, req)
        if score > 0:
            estimated_total = product.price * Decimal(str(req.pipe_length_m))
            category_name = product.category.name if product.category else None
            results.append(RecommendationItem(
                product_id=product.id,
                product_name=product.name,
                unit_price=product.price,
                estimated_total=estimated_total,
                category_name=category_name,
                match_score=score,
                reasons=reasons
            ))

    results.sort(key=lambda x: x.match_score, reverse=True)

    query_summary = (
        f"جستجو برای لوله قطر {req.diameter_mm}mm"
        f"{f' از جنس {req.material}' if req.material else ''}"
        f" طول {req.pipe_length_m}m"
        f"{f' بودجه {req.budget:,.0f} تومان' if req.budget else ''}"
    )

    return RecommendationResponse(
        query_summary=query_summary,
        recommendations=results[:5],
        engineering_notes=get_engineering_notes(req)
    )
