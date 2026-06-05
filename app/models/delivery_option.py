from sqlalchemy import Column, Integer, String

from app.db.base import Base


class DeliveryOption(Base):
    __tablename__ = "delivery_options"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(100), nullable=False)

    description = Column(String(255), nullable=False)

    charge = Column(Integer, nullable=False)

    delivery_days = Column(Integer, nullable=True)