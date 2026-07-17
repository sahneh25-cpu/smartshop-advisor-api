from fastapi import FastAPI
from app.core.database import Base, engine
from app.api.routes import cat_router, prod_router
from app.api.recommendations import router as rec_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="SmartShop Advisor",
    description="API مشاوره محصولات لولهکشی",
    version="1.0.0"
)

app.include_router(cat_router)
app.include_router(prod_router)
app.include_router(rec_router, prefix="/recommendations", tags=["Recommendations"])
