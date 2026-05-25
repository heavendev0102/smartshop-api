from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field


class CartItemCreate(BaseModel):
    product_id: int = Field(..., gt=0)
    quantity: int = Field(1, gt=0)


class CartItemUpdate(BaseModel):
    quantity: int = Field(..., gt=0)


class CartProductSummary(BaseModel):
    id: int
    name: str
    image_url: Optional[str] = None
    current_price: Decimal
    stock: int = 0

    class Config:
        from_attributes = True


class CartItemResponse(BaseModel):
    id: int
    product_id: int
    quantity: int
    product: CartProductSummary
    line_total: Decimal
    created_date: datetime
    modified_date: datetime

    class Config:
        from_attributes = True


class CartResponse(BaseModel):
    items: list[CartItemResponse] = []
    item_count: int = 0
    subtotal: Decimal = Decimal("0.00")
