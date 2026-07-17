from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.core.database import Base

class Attribute(Base):
    __tablename__ = "attributes"

    id = Column(Integer, primary_key=True, index=True)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    name = Column(String(100), nullable=False)
    display_name = Column(String(200), nullable=False)
    question_text = Column(String(500), nullable=True)
    attribute_type = Column(String(50), nullable=False)  # numeric/boolean/single_choice/multi_choice
    options = Column(JSON, nullable=True)
    is_required = Column(Boolean, default=False)
    sort_order = Column(Integer, default=0)

    category = relationship("Category", back_populates="attributes")
