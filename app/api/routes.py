from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel, Field, condecimal
from decimal import Decimal
from app.core.database import get_db
from app.models.product import Product

router = APIRouter(prefix="/products", tags=["Products"])


# ----------- Pydantic Schemas -----------

class ProductCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, examples=["لپ‌تاپ ایسوس"])
    price: condecimal(gt=Decimal('0'), max_digits=10, decimal_places=2) = Field(..., examples=[25000.50])
    description: str | None = Field(None, max_length=500, examples=["توضیحات مربوط به محصول"])


class ProductUpdate(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=100)
    price: condecimal(gt=Decimal('0'), max_digits=10, decimal_places=2) | None = None
    description: str | None = Field(None, max_length=500)


class ProductResponse(BaseModel):
    id: int
    name: str
    price: Decimal
    description: str | None

    class Config:
        from_attributes = True


# ----------- Endpoints -----------

@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    db_product = Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


@router.get("/", response_model=List[ProductResponse])
def get_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    safe_limit = min(limit, 100)
    return db.query(Product).offset(skip).limit(safe_limit).all()


@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product


@router.put("/{product_id}", response_model=ProductResponse)
def update_product(product_id: int, product: ProductUpdate, db: Session = Depends(get_db)):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    
    update_data = product.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_product, key, value)
        
    db.commit()
    db.refresh(db_product)
    return db_product


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    db.delete(db_product)
    db.commit()
    return None
