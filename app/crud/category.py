# app/crud/category.py

from sqlalchemy.orm import Session
from app.models.category import Category  # <--- اصلاح اصلی: آدرس دهی مطلق به مدل
from app.schemas.category import CategoryCreate, CategoryUpdate # <--- اصلاح اصلی: آدرس دهی مطلق به اسکیما

# تابع برای گرفتن یک دسته بندی
def get(db: Session, category_id: int):
    return db.query(Category).filter(Category.id == category_id).first()

# تابع برای گرفتن لیستی از دسته بندی ها
def get_all(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Category).offset(skip).limit(limit).all()

# تابع برای ایجاد دسته بندی جدید
def create(db: Session, category: CategoryCreate):
    db_category = Category(
        name=category.name,
        description=category.description,
        parent_id=category.parent_id
    )
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

# تابع برای آپدیت کردن دسته بندی
def update(db: Session, *, db_obj: Category, obj_in: CategoryUpdate):
    # تبدیل Pydantic model به دیکشنری
    update_data = obj_in.model_dump(exclude_unset=True)
    # آپدیت کردن فیلدهای db_obj
    for field in update_data:
        setattr(db_obj, field, update_data[field])
    
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

# تابع برای حذف دسته بندی
def remove(db: Session, *, id: int):
    obj = db.query(Category).get(id)
    db.delete(obj)
    db.commit()
    return obj
