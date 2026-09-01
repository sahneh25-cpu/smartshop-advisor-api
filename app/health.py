from fastapi import APIRouter

router = APIRouter()

@router.get("/health", tags=["Health"])
def health():
    return {"status": "ok", "service": "smartshop-advisor-api", "version": "2.0.0"}
