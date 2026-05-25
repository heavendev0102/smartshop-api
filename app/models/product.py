from datetime import datetime, timezone

from sqlalchemy import Boolean, Column, DateTime, Integer, Numeric, String, Text
from sqlalchemy.orm import relationship

from app.db.base import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    image_url = Column(String, nullable=True)
    current_price = Column(Numeric(10, 2), nullable=False)
    original_price = Column(Numeric(10, 2), nullable=True)
    discount_percent = Column(Integer, nullable=True)
    description = Column(Text, nullable=True)
    stock = Column(Integer, nullable=False, default=0)
    ratings = Column(Numeric(3, 2), nullable=True)
    is_active = Column(Boolean, default=True)
    created_date = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    modified_date = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    product_categories = relationship("ProductCategory", back_populates="product", cascade="all, delete-orphan")
    product_sections = relationship("ProductSection", back_populates="product", cascade="all, delete-orphan")
    reviews = relationship("ProductReview", back_populates="product", cascade="all, delete-orphan")
