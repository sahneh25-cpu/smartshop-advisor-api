from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from app.core.database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    name = Column(String(300), nullable=False)
    price = Column(Integer, nullable=True)
    description = Column(Text, nullable=True)
    attributes = Column(JSONB, nullable=True, default=dict)

    category = relationship("Category", back_populates="products")
