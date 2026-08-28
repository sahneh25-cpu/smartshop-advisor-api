from fastapi import FastAPI
from app.core.database import Base, engine
from app.api.routes import cat_router, prod_router
from app.api.recommendations import router as rec_router
from app.api.search import router as search_router
from app.api.advise import router as advise_router
from app.api.ai import router as ai_router
from app.api.agent import router as agent_router
from app.api.agent import router as agent_router

# Create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="SmartShop Advisor",
    description="SmartShop Advisor API",
    version="2.0.0"
)

app.include_router(cat_router)
app.include_router(prod_router)
app.include_router(rec_router, prefix="/recommendations", tags=["Recommendations"])
app.include_router(search_router, prefix="/search", tags=["Search"])
app.include_router(advise_router, prefix="/api/v1", tags=["Advise"])
app.include_router(ai_router)
app.include_router(agent_router)

@app.get("/", tags=["Health"])
def root():
    return {"status": "ok", "version": "2.0.0"}
