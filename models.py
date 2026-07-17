# C:\Users\Mohammadi\smartshop-advisor\models.py (نسخه نهایی و اصلاح شده)

# تغییر ۱: Float حذف شد و Numeric به انتهای لیست اضافه شد
from sqlalchemy import Column, Integer, String, ForeignKey, Numeric 
from sqlalchemy.orm import relationship
from database import Base

class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=True)
    products = relationship("Product", back_populates="category")


class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    # تغییر ۲: نوع ستون price از Float به Numeric(10, 2) تغییر کرد
    price = Column(Numeric(10, 2), nullable=False) 
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    category = relationship("Category", back_populates="products")

