from fastapi import FastAPI
from app.api.routes import router as product_router
from app.routers.categories import router as category_router

app = FastAPI(title="SmartShop Advisor API", version="1.0.0")

app.include_router(product_router)
app.include_router(category_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to SmartShop Advisor API"}
