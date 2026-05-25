from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field


class WishlistItemCreate(BaseModel):
    product_id: int = Field(..., gt=0)


class WishlistProductSummary(BaseModel):
    id: int
    name: str
    image_url: Optional[str] = None
    current_price: Decimal
    stock: int = 0
    ratings: Optional[Decimal] = None

    class Config:
        from_attributes = True


class WishlistItemResponse(BaseModel):
    id: int
    product_id: int
    product: WishlistProductSummary
    created_date: datetime

    class Config:
        from_attributes = True


class WishlistCheckResponse(BaseModel):
    product_id: int
    in_wishlist: bool
    wishlist_item_id: Optional[int] = None
