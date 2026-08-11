from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate

class CRUDProduct:
    def get(self, db: Session, product_id: int):
        return db.query(Product).filter(Product.id == product_id).first()

    def get_multi(self, db: Session, *, skip=0, limit=100,
                  category_id=None, search=None, min_price=None, max_price=None):
        q = db.query(Product)
        if category_id:
            q = q.filter(Product.category_id == category_id)
        if search:
            term = f"%{search}%"
            q = q.filter(or_(Product.name.ilike(term), Product.description.ilike(term)))
        if min_price is not None:
            q = q.filter(Product.price >= min_price)
        if max_price is not None:
            q = q.filter(Product.price <= max_price)
        return q.offset(skip).limit(limit).all()

    def create(self, db: Session, *, obj_in: ProductCreate):
        obj = Product(**obj_in.model_dump())
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    def update(self, db: Session, *, db_obj: Product, obj_in: ProductUpdate):
        for k, v in obj_in.model_dump(exclude_unset=True).items():
            setattr(db_obj, k, v)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, product_id: int):
        obj = db.query(Product).filter(Product.id == product_id).first()
        if obj:
            db.delete(obj)
            db.commit()
        return obj

product = CRUDProduct()
