# app/api/endpoints/category.py

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

# ---===[ بخش اصلاح شده وارد کردن ماژول ها ]===---
# ما به صورت مستقیم توابع CRUD و مدل های Schema را وارد می کنیم
# این کار کد را خواناتر و خطایابی را ساده تر می کند
from app.crud.category import get, get_all, create, update, remove
from app.schemas.category import Category, CategoryCreate, CategoryUpdate
from app.api import deps
# ---=======================================---

router = APIRouter()

@router.post("/", response_model=Category, status_code=status.HTTP_201_CREATED)
def create_category(
    *,
    db: Session = Depends(deps.get_db),
    category_in: CategoryCreate,
):
    """
    ایجاد یک دسته بندی جدید
    """
    # حالا به صورت مستقیم از تابع create استفاده می کنیم
    category = create(db=db, category=category_in)
    return category

@router.get("/", response_model=List[Category])
def read_categories(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
):
    """
    دریافت لیست دسته بندی ها
    """
    # استفاده مستقیم از get_all
    categories = get_all(db, skip=skip, limit=limit)
    return categories

@router.get("/{category_id}", response_model=Category)
def read_category(
    *,
    db: Session = Depends(deps.get_db),
    category_id: int,
):
    """
    دریافت یک دسته بندی خاص با شناسه
    """
    # استفاده مستقیم از get
    category = get(db=db, category_id=category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Category not found"
        )
    return category

@router.put("/{category_id}", response_model=Category)
def update_category(
    *,
    db: Session = Depends(deps.get_db),
    category_id: int,
    category_in: CategoryUpdate,
):
    """
    آپدیت کردن یک دسته بندی
    """
    category = get(db=db, category_id=category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found",
        )
    # استفاده مستقیم از update
    category = update(db=db, db_obj=category, obj_in=category_in)
    return category

@router.delete("/{category_id}", response_model=Category)
def delete_category(
    *,
    db: Session = Depends(deps.get_db),
    category_id: int,
):
    """
    حذف یک دسته بندی
    """
    category = get(db=db, category_id=category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found",
        )
    # استفاده مستقیم از remove
    category = remove(db=db, id=category_id)
    return category
