from datetime import datetime
from decimal import Decimal
from typing import List, Optional

from pydantic import BaseModel, Field


class CategoryResponse(BaseModel):
    id: int
    name: str
    slug: str
    icon_url: Optional[str] = None
    description: Optional[str] = None
    display_order: int = 0
    is_active: bool = True

    class Config:
        from_attributes = True


class SectionResponse(BaseModel):
    id: int
    name: str
    slug: str
    description: Optional[str] = None
    display_order: int = 0
    is_active: bool = True

    class Config:
        from_attributes = True


class ProductCreate(BaseModel):
    name: str
    image_url: Optional[str] = None
    description: Optional[str] = None
    stock: int = 0
    current_price: Decimal
    original_price: Optional[Decimal] = None
    discount_percent: Optional[int] = None
    category_slugs: List[str] = Field(
        ...,
        description="Browse category: phones, smartwatches, cameras, headphones, computers, gaming",
    )
    section_slugs: List[str] = Field(
        default_factory=list,
        description="Homepage tab: new_arrivals, bestsellers, featured",
    )


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    image_url: Optional[str] = None
    description: Optional[str] = None
    stock: Optional[int] = None
    current_price: Optional[Decimal] = None
    original_price: Optional[Decimal] = None
    discount_percent: Optional[int] = None
    is_active: Optional[bool] = None
    category_slugs: Optional[List[str]] = None
    section_slugs: Optional[List[str]] = None


class ProductCategoryAssign(BaseModel):
    category_slugs: List[str]


class ProductSectionAssign(BaseModel):
    section_slugs: List[str]


class ProductReviewResponse(BaseModel):
    id: int
    product_id: int
    user_id: int
    rating: int
    comment: Optional[str] = None
    created_date: datetime

    class Config:
        from_attributes = True


class RatingSummaryResponse(BaseModel):
    average_rating: Optional[Decimal] = None
    total_reviews: int = 0
    rating_counts: dict[int, int] = Field(
        default_factory=lambda: {1: 0, 2: 0, 3: 0, 4: 0, 5: 0},
        description="Count of reviews per star rating (1-5)",
    )


class ProductResponse(BaseModel):
    id: int
    name: str
    image_url: Optional[str] = None
    description: Optional[str] = None
    stock: int = 0
    ratings: Optional[Decimal] = None
    current_price: Decimal
    original_price: Optional[Decimal] = None
    discount_percent: Optional[int] = None
    is_active: bool
    categories: List[CategoryResponse] = []
    sections: List[SectionResponse] = []
    created_date: datetime
    modified_date: datetime

    class Config:
        from_attributes = True


class SectionWithProductsResponse(BaseModel):
    name: str
    slug: str
    products: List[ProductResponse] = []


class StorefrontResponse(BaseModel):
    categories: List[CategoryResponse] = []
    new_arrivals: SectionWithProductsResponse
    bestsellers: SectionWithProductsResponse
    featured: SectionWithProductsResponse
