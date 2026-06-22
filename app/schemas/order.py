from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel


class OrderPreviewRequest(BaseModel):
    address_id: int
    delivery_option_id: int
    delivery_date: date | None = None


class OrderPreviewResponse(BaseModel):
    address: str
    shipment_method: str
    subtotal: Decimal
    estimated_tax: Decimal
    shipping_charge: Decimal
    total: Decimal


class OrderCreateRequest(BaseModel):
    address_id: int
    delivery_option_id: int
    delivery_date: date | None = None
    payment_method: str


class OrderCreateResponse(BaseModel):
    order_id: int
    order_status: str
    subtotal: Decimal
    estimated_tax: Decimal
    shipping_charge: Decimal
    total: Decimal

class OrderDetailsResponse(BaseModel):
    order_id: int
    payment_method: str
    amount_paid: Decimal
    estimated_delivery: date | None
    order_status: str

class OrderHistoryProductResponse(BaseModel):
    product_id: int
    product_name: str
    quantity: int
    unit_price: Decimal
    line_total: Decimal


class OrderHistoryResponse(BaseModel):
    order_id: int
    order_status: str
    payment_method: str
    total: Decimal
    delivery_date: date | None
    created_date: datetime
    products: list[OrderHistoryProductResponse]