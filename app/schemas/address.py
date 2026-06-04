from pydantic import BaseModel
from datetime import datetime


class AddressCreate(BaseModel):
    title: str
    phone: str
    address: str
    status: str

class AddressUpdate(BaseModel):
    title: str
    phone: str
    address: str
    status: str

class AddressResponse(BaseModel):
    id: int
    title: str
    phone: str
    address: str
    status: str
    address: str
    created_date: datetime
    modified_date: datetime

    class Config:
        from_attributes = True