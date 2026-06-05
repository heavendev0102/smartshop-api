from datetime import date

from pydantic import BaseModel


class DeliveryOptionResponse(BaseModel):
    id: int
    name: str
    description: str
    charge: int
    delivery_days: int | None
    estimated_delivery_date: date | None

    class Config:
        from_attributes = True